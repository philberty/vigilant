import socket

class UDPStatsTransport:
    def __init__(self, host='localhost', port=8080):
        self._host = host
        self._port = port

    def initTransport(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def postMessageOnTransport(self, message):
        if type(message) is not bytes:
            raise Exception('Data must be in bytes')
        self._sock.sendto(message, (self._host, self._port))
