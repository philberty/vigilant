import unittest

from StatsCore import SimpleTransports

class UDPTransportTests(unittest.TestCase):

    _port = 1234

    def setUp(self):
        self._transport = SimpleTransports.UDPStatsTransport(1234)

    def testThatPostMessageShouldRaiseExceptionOnAnythingButBytes(self):
        pass