#!/usr/bin/env python3

import time

import StatsCore
from StatsCore import SimpleTransports

def test():
    transport = SimpleTransports.UDPStatsTransport()
    client = StatsCore.attachOrCreateStatsDaemon('test', transport)
    time.sleep(10)
    client.postStopDaemon()
    client.close()

if __name__ == "__main__":
    test()