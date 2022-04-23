from UBloxReaderDEMUX import UBloxReaderDEMUX
from UBloxWriterMUX import UBloxWriterMUX
from UBloxStream import UBloxStream


class StreamMuxDemux:
    def __init__(self, serial, ttl=1):
        self._readerDEMUX = UBloxReaderDEMUX(serial, ttl, serial.timeout)
        self._writerMUX = UBloxWriterMUX(serial)
        self._nmea = UBloxStream(
            self._readerDEMUX.readNMEA, self._writerMUX.writeNMEA, self)
        self._ubx = UBloxStream(self._readerDEMUX.readUBX,
                                self._writerMUX.writeUBX, self)
        self._rtcm = UBloxStream(
            self._readerDEMUX.readRTCM, self._writerMUX.writeRTCM, self)
        self._closed = False

    def _validate(self):
        if self._closed:
            raise ValueError("Use of a closed StreamMuxDemux")

    def close(self):
        if self._closed:
            return
        self._closed = True
        self._readerDEMUX.close()
        self._writerMUX.close()

    def is_closed(self):
        return self._closed

    @property
    def UBX(self):
        self._validate()
        return self._ubx

    @property
    def NMEA(self):
        self._validate()
        return self._nmea

    @property
    def RTCM(self):
        self._validate()
        return self._rtcm
