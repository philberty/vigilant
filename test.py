#!/usr/bin/env python3
import time

import StatsClient

from StatsClient import StatsDaemon
from StatsClient import SimpleTransports

def StatsClientMain():
    transport = SimpleTransports.UDPStatsTransport()
    client = StatsClient.attachOrCreateStatsDaemon('test', transport)

    pid = StatsDaemon.getPidFromLockFile()

    time.sleep(20)
    print('sending daemon kill')
    client.postStopDaemon()

    time.sleep(1)

    if pid > 0:
        try:
            import os
            os.kill(pid, 0)
            raise Exception('Daemon [%i] has not stopped' % pid)
        except:
            pass

if __name__ == "__main__":
    StatsClientMain()