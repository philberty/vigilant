import json
import socket
import datetime


def get_time_stamp():
    return str(datetime.datetime.now())


class Transport:
    def post(self, message: bytes):
        pass

    def post_message_on_transport(self, message: dict):
        message['ts'] = get_time_stamp()
        self.post(json.dumps(message).encode('utf-8'))


class UDPStatsTransport(Transport):
    def __init__(self, host='localhost', port=8080):
        self._host = host
        self._port = port
        self._sock = None

    def status(self):
        return 'UDP Transport %s:%i' % (self._host, self._port)

    def init_transport(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setblocking(True)

    def post(self, message: bytes):
        self._sock.sendto(message, (self._host, self._port))


class TCPStatsTransport(Transport):
    def __init__(self, host='localhost', port=8080):
        self._host = host
        self._port = port
        self._sock = None

    def status(self):
        return 'TCP Transport %s:%i' % (self._host, self._port)

    def init_transport(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((self._host, self._port))

    def post(self, message: bytes, exception=None, retry=0):
        if retry > 2:
            raise exception
        try:
            self._sock.send(message)
        except Exception as e:
            self.init_transport()
            self.post(message, exception=e, retry=retry + 1)

