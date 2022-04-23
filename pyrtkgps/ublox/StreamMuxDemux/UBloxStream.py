class UBloxStream():
    def __init__(self, read_func, write_func, stream_mux_demux):
        self._read = read_func
        self._write = write_func
        self._stream_mux_demux = stream_mux_demux

    def read(self, n=1):
        result = b""
        for _ in range(n):
            result += self._read()
        return result

    def readline(self):
        byte = self._read()
        result = byte
        while byte != b'\n':
            byte = self._read()
            result += byte
        return result

    def write(self, data):
        self._write(data)

    @property
    def owner(self):
        return self._stream_mux_demux
