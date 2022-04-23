from threading import Thread
from UBloxQueue import UBloxQueue
from StreamMuxDemuxError import StreamMuxDemuxError


class UBloxReaderDEMUX:
    def __init__(self, serial, ttl, timeout, onError=None):
        self._serial = serial

        self._nmea_q = UBloxQueue(ttl, timeout)
        self._ubx_q = UBloxQueue(ttl, timeout)
        self._rtcm_q = UBloxQueue(ttl, timeout)

        self._onError = onError

        self._closed = False
        self._reader_thread = Thread(target=self._read_to_queue)
        self._reader_thread.daemon = True
        self._reader_thread.start()

    def _validate(self):
        if self._closed:
            raise StreamMuxDemuxError("Use of a closed UBloxReaderDEMUX")

    def _read_to_queue(self):
        error = None
        try:
            self._real_read_to_queue()

        # TODO: change exception type to only serial exceptions
        except Exception as e:
            self.close()
            error = e

        if error:
            raise StreamMuxDemuxError(error)

    def _real_read_to_queue(self):
        self._validate()
        ser = self._serial

        while not self._closed:
            frame = [ser.read()]

            # NMEA
            if frame[0] == b"$":
                frame.append(ser.readline())

                # entire message
                msg = b"".join(frame)

                # add msg to NMEA queue
                for byte in msg:
                    if self._nmea_q.is_closed():
                        break
                    self._nmea_q.put(byte.to_bytes(1, 'big'))

                # done
                continue

            # UBX
            if frame[0] == b"\xb5":
                frame.append(ser.read())
                if frame[1] == b"\x62":
                    frame.append(ser.read())                # class
                    frame.append(ser.read())                # id
                    length_bytes = ser.read(2)              # length
                    frame.append(length_bytes)

                    length = int.from_bytes(
                        length_bytes, byteorder='little', signed=False)
                    frame.append(ser.read(length))          # payload
                    frame.append(ser.read())                # CK_A
                    frame.append(ser.read())                # CK_B

                    # entire message
                    msg = b"".join(frame)

                    # add msg to UBX queue
                    for byte in msg:
                        if self._ubx_q.is_closed():
                            break
                        self._ubx_q.put(byte.to_bytes(1, 'little'))

                    # done
                    continue

            # RTCM
            if frame[0] == b"\xD3":
                frame.append(ser.read())                    # byte 2
                frame.append(ser.read())                    # byte 3

                num1 = int.from_bytes(
                    frame[1], byteorder='little', signed=False)
                num2 = int.from_bytes(
                    frame[2], byteorder='little', signed=False)
                length = ((num1 & 0b00000011) << 8) + num2
                frame.append(ser.read(length))              # payload
                frame.append(ser.read(3))                   # parity

                # entire message
                msg = b"".join(frame)

                # add msg to UBX queue
                for byte in msg:
                    if self._rtcm_q.is_closed():
                        break
                    self._rtcm_q.put(byte.to_bytes(1, 'little'))

                # done
                continue

            # error
            if self._onError:
                data = b"".join(frame)
                self._onError(data)

    def readNMEA(self):
        self._validate()
        return self._nmea_q.get()

    def readUBX(self):
        self._validate()
        return self._ubx_q.get()

    def readRTCM(self):
        self._validate()
        return self._rtcm_q.get()

    def close(self):
        if self._closed:
            return
        self._closed = True
        self._nmea_q.close()
        self._ubx_q.close()
        self._rtcm_q.close()

        try:
            self._reader_thread.join()
        except Exception:
            pass

    def is_closed(self):
        return self._closed
