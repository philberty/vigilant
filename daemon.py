#!/usr/bin/env python3

import sys
import logging
import logging.config

import optparse
import StatsCore

from StatsCore import StatsDaemonState
from StatsCore import SimpleTransports

from configparser import RawConfigParser as CParser


def printVersion():
    print('%s version %s' % (StatsDaemonState.STATS_DAEMON_APP, StatsDaemonState.STATS_DAEMON_VERSION))


def isDaemonRunning(config):
    try:
        lock = str(config.get('daemon', 'lock'))
        sock = str(config.get('daemon', 'sock'))
        client = StatsCore.attchToStatsDaemon(pid=lock, sock=sock)
        client.close()
        return True
    except:
        return str(sys.exc_info()[1])


def killDaemon(config):
    lock = str(config.get('daemon', 'lock'))
    sock = str(config.get('daemon', 'sock'))
    client = StatsCore.attchToStatsDaemon(pid=lock, sock=sock)
    client.postStopDaemon()
    client.close()


def transportFromConfig(config):
    transport = str(config.get('server', 'transport'))
    if transport == 'udp':
        host = str(config.get('server', 'host'))
        port = int(config.get('server', 'port'))
        return SimpleTransports.UDPStatsTransport(host=host, port=port)
    else:
        raise Exception('Invalid transport in configuration')


def startDaemon(config):
    lock = str(config.get('daemon', 'lock'))
    sock = str(config.get('daemon', 'sock'))
    key = str(config.get('daemon', 'key'))
    transport = transportFromConfig(config)
    client = StatsCore.attachOrCreateStatsDaemon(key, transport, pid=lock, sock=sock)
    client.close()


def configureLogging(config):
    try:
        logging.config.fileConfig(config)
    except:
        sys.exit("invalid config present in [%s] - [%s]" % (config, sys.exc_info()))


def daemon():
    parser = optparse.OptionParser()
    parser.add_option("-v", "--version", dest='version',
                      help="Print version", action="store_true")
    parser.add_option("-c", "--config", dest="config",
                      help="Config file location", default=None)
    parser.add_option("-r", "--status", dest="status",
                      help="Is daemon running", default=False, action="store_true")
    parser.add_option('-s', "--start", dest="start",
                      help="Start Daemon with config", default=False, action="store_true")
    parser.add_option('-k', "--kill", dest="kill",
                      help="Kill stats daemon", default=False, action="store_true")
    options, _ = parser.parse_args()
    configureLogging(options.config)
    if options.version is True:
        printVersion()
        return
    if options.config is None:
        sys.exit('You must specify a configuration file, see --help')
    config = CParser()
    config.read(options.config)
    if options.status:
        print(isDaemonRunning(config))
    if options.kill:
        killDaemon(config)
    if options.start:
        startDaemon(config)


if __name__ == "__main__":
    daemon()