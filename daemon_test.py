#!/usr/bin/env python3

import os
import time
import daemon
import socket
import StatsCore

from configparser import RawConfigParser as CParser


def test():
    config = CParser()
    config.read('./etc/observant/observant.cfg')

    pid = os.fork()
    if pid != 0:
        os.waitpid(pid, 0)
    else:
        dump = './.test.out'
        sockPath = './.test.sock'
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.setblocking(0)
        with open(dump, 'w') as fd:
            fd.write("test")
            server.bind(sockPath)
            server.listen(1)
            transport = daemon.transportFromConfig(config)
            lock = str(config.get('daemon', 'lock'))
            sock = str(config.get('daemon', 'sock'))
            key = str(config.get('daemon', 'key'))
            client = StatsCore.attachOrCreateStatsDaemon(key, transport, pid=lock, sock=sock)
            client.postWatchPid('test', os.getpid())
            time.sleep(4)
            client.postLogMessageForKey('test', 'some random logmessage')
            time.sleep(4)
            client.postLogMessageForKey('test', 'some random logmessage')
            client.close()
            time.sleep(4)
        os.remove(dump)
        server.close()
        os.unlink(sockPath)

if __name__ == "__main__":
    test()
