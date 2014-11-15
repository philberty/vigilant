#!/usr/bin/env python3

import StatsClient
from StatsClient import SimpleTransports

def StatsClientMain():
    transport = SimpleTransports.UDPStatsTransport()
    client = StatsClient.attachOrCreateStatsDaemon('test', transport)
    client.postStopWatchPid(1234)

if __name__ == "__main__":
    StatsClientMain()