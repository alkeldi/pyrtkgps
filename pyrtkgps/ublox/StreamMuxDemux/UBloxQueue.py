import time
from queue import Queue
from threading import Thread

from pyrtkgps.ublox.StreamMuxDemux.StreamMuxDemuxError import StreamMuxDemuxError


class UBloxQueue():
    def __init__(self, ttl, timeout):
        self._q = Queue()
        self._max_ttl = ttl
        self._timeout = timeout

        self._closed = False
        self._watcher_thread = Thread(target=self._watch_old_items)
        self._watcher_thread.daemon = True
        self._watcher_thread.start()

    def _validate(self):
        if self._closed:
            raise StreamMuxDemuxError("Use of a closed UBloxQueue")

    def _watch_old_items(self):
        self._validate()
        while not self._closed:
            ttl = self._discard_old_items()
            time.sleep(ttl)

    def _discard_old_items(self):
        self._validate()
        now = time.time()
        while self._q.qsize() > 0:
            _, expires_at = self._q.queue[-1]
            if expires_at <= now:
                self._q.get()
            else:
                ttl = expires_at - now
                return ttl
        return self._max_ttl

    def put(self, item):
        self._validate()
        expires_at = time.time() + self._max_ttl
        self._q.put((item, expires_at))

    def get(self):
        self._validate()
        get_at = time.time()
        try:
            item, expires_at = self._q.get(True, self._timeout)
            while expires_at <= get_at:
                item, expires_at = self._q.get(True, self._timeout)
            return item
        # TODO only handle timeout exceptions
        except Exception:
            return b''

    def close(self):
        if self._closed:
            return
        self._closed = True
        self._watcher_thread.join()

    def is_closed(self):
        return self._closed
