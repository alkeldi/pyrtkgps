from queue import Queue
from threading import Thread

from pyrtkgps.ublox.StreamMuxDemux.StreamMuxDemuxError import StreamMuxDemuxError


class UBloxWriterMUX:
    def __init__(self, serial):
        self._serial = serial
        self._q = Queue()

        self._closed = False
        self._writer_thread = Thread(target=self._write_from_queue)
        self._writer_thread.daemon = True
        self._writer_thread.start()

    def _validate(self):
        if self._closed:
            raise StreamMuxDemuxError("Use of a closed UBloxWriterMUX")

    def _write_from_queue(self):
        error = None
        try:
            self._real_write_from_queue()
        # TODO: change exception type to only serial exceptions
        except Exception as e:
            self.close()
            error = e

        if error:
            raise StreamMuxDemuxError(error)

    def _real_write_from_queue(self):
        self._validate()
        while not self._closed:
            try:
                msg = self._q.get(timeout=1)
            # TODO: change exception type to only timeout exceptions
            except Exception:
                continue

            self._serial.write(msg)

    def writeNMEA(self, data):
        self._validate()
        self._q.put(data)

    def writeUBX(self, data):
        self._validate()
        self._q.put(data)

    def writeRTCM(self, data):
        self._validate()
        self._q.put(data)

    def close(self):
        if self._closed:
            return
        self._closed = True
        try:
            self._writer_thread.join()
        except Exception:
            pass

    def is_closed(self):
        return self._closed
