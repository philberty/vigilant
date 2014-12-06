#!/usr/bin/env python3

import sys
import logging
import optparse

import StatsBoard

from configparser import RawConfigParser as CParser


def setup_logging(config):
    import logging.config

    try:
        logging.config.fileConfig(config)
    except:
        pass


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
    bind = str(config.get('dashboard', 'bind'))
    port = int(config.get('dashboard', 'port'))
    stores = str(config.get('dashboard', 'datastores'))
    stores = [i.strip() for i in stores.split(',')]
    StatsBoard.StatsBoardServer(bind, port, stores).listen()


if __name__ == "__main__":
    dashboard()