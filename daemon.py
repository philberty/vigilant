#!/usr/bin/env python3
import time

import StatsCore

from StatsCore import StatsDaemon
from StatsCore import SimpleTransports

def StatsClientMain():
    transport = SimpleTransports.UDPStatsTransport()
    client = StatsCore.attachOrCreateStatsDaemon('test', transport)

    time.sleep(10)
    print('sending daemon kill')
    client.postStopDaemon()

if __name__ == "__main__":
    StatsClientMain()