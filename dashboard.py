#!/usr/bin/env python3

import os
import sys
import logging
import optparse

import StatsCore
import StatsBoard

from configparser import RawConfigParser as CParser


def setup_logging(config):
    import logging.config

    try:
        logging.config.fileConfig(config)
    except:
        pass


def setup_monitoring(config):
    try:
        name = "observant-dashboard-%s" % str(config.get("dashboard", "port"))
        client = StatsCore.attchToStatsDaemon()
        client.postWatchPid(name, os.getpid())
        client.close()
    except:
        logging.error("Unable to setup monitoring: [%s]" % str(sys.exc_info()))


def dashboard():
    parser = optparse.OptionParser()
    parser.add_option("-c", "--config", dest="config",
                      help="Config file location", default=None)
    options, _ = parser.parse_args()
    setup_logging(options.config)
    if options.config is None:
        sys.exit('You must specify a configuration file, see --help')
    config = CParser()
    config.read(options.config)
    setup_monitoring(config)
    bind = str(config.get('dashboard', 'bind'))
    port = int(config.get('dashboard', 'port'))
    StatsBoard.StatsBoardServer(bind, port).listen()


if __name__ == "__main__":
    dashboard()
