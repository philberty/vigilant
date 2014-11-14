import socket

class UDPStatsTransport:
    def __init__(self, host='localhost', port=8080):
        self._host = host
        self._port = port

    def _createSocket(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return self._sock.fileno()

    def initTransport(self):
        self._createSocket()

    def postMessageOnTransport(self, message):
        if type(message) is not bytes:
            raise Exception('Data must be in bytes')
        self._sock.send(message)
