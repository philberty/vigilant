#!/usr/bin/env python3

import os
import time
import daemon
import StatsCore

from configparser import RawConfigParser as CParser


def test():
    config = CParser()
    config.read('./etc/observant/observant.cfg')

    pid = os.fork()
    if pid != 0:
        os.waitpid(pid, 0)
    else:
        transport = daemon.transportFromConfig(config)
        lock = str(config.get('daemon', 'lock'))
        sock = str(config.get('daemon', 'sock'))
        key = str(config.get('daemon', 'key'))
        client = StatsCore.attachOrCreateStatsDaemon(key, transport, pid=lock, sock=sock)
        client.postWatchPid('test', os.getpid())
        time.sleep(4)
        for i in range(3):
            client.postLogMessageForKey('test', 'some random logmessage')
        time.sleep(4)
        client.close()
        time.sleep(4)

if __name__ == "__main__":
    test()
