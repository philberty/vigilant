#!/usr/bin/env python

import os
import sys
import json
import time
import unittest

if len (sys.argv) < 2:
    sys.exit ('Error: need to pass prefix to pywatchy.so python module')
__path = '%(prefix)s/lib/python%(major)s.%(minor)s/site-packages/' \
    % {'prefix' : sys.argv [1], 'major' : sys.version_info [0],
       'minor' : sys.version_info [1] }
sys.path.append (__path)
import pywatchy

from WatchyServer import StatsApp
from WatchyServer import StatsAggregator

class WatchyTestCase (unittest.TestCase):

    def setUp (self):
        local_fifo = os.path.join (os.getcwd (), 'fifo.watchy')
        try:
            f = open (local_fifo)
            raise Exception ('test directory not clean')
        except IOError:
            pass
        assert local_fifo
        StatsApp.app.config ['TESTING'] = True
        self.app = StatsApp.app.test_client()
        self.daemon = pywatchy.WatchyDaemon ('localhost', 7878, fifo=local_fifo)
        self.udp_server = StatsAggregator.UDPStatsServer (host='localhost', port=7878)
        self.udp_server.start ()

    def tearDown (self):
        self.daemon.cleanup ()

    def test_logs (self):
        resp = self.app.get ('/api/logs/keys')
        assert resp.status_code == 200
        data = json.loads (resp.data)
        assert len (data['keys']) == 0
        for i in range (5):
            self.daemon.postMessage ('test', 'Hello World')
        time.sleep (1)
        resp = self.app.get ('/api/logs/keys')
        assert resp.status_code == 200
        data = json.loads (resp.data)
        assert len (data ['keys']) == 1
        assert data ['keys'] [0] == 'test'

if __name__ == '__main__':
    del sys.argv [1:]
    unittest.main ()
