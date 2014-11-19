#!/usr/bin/env python3
import time

import StatsClient

from StatsClient import StatsDaemon
from StatsClient import SimpleTransports

def StatsClientMain():
    transport = SimpleTransports.UDPStatsTransport()
    client = StatsClient.attachOrCreateStatsDaemon('test', transport)

    time.sleep(10)
    print('sending daemon kill')
    client.postStopDaemon()

if __name__ == "__main__":
    StatsClientMain()