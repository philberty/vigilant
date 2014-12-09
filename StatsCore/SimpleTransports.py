import json
import socket
import datetime


def get_time_stamp():
    return str(datetime.datetime.now())


class UDPStatsTransport:
    def __init__(self, host='localhost', port=8080):
        self._host = host
        self._port = port

    def status(self):
        return 'UDP Transport %s:%i' % (self._host, self._port)

    def initTransport(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def postMessageOnTransport(self, message):
        message['ts'] = get_time_stamp()
        message = json.dumps(message).encode('utf-8')
        self._sock.sendto(message, (self._host, self._port))
