#!/usr/bin/env python

import os
import sys
import logging
import optparse
import traceback
import logging.config

from WatchyServer import ServerUtil
from WatchyServer import StatsServer
from WatchyServer import BackendUtil

from ConfigParser import RawConfigParser as CParser

def printVersion ():
    print "WatchyD Version [%s]" % ServerUtil.version

def serverMain ():
    global _spid, _rpid
    parser = optparse.OptionParser ()
    parser.add_option ("-v", "--version", dest='version',
                       help="Print version", action="store_true")
    parser.add_option ("-l", "--logfile", dest='logfile',
                       help="Ouput logfile", default="./server.log")
    parser.add_option ("-c", "--config", dest="config",
                       help="Config file location", default=None)
    parser.add_option ("-F", "--fork", dest="fork", action="store_true",
                       help="Fork as daemon", default=False)
    (options, args) = parser.parse_args ()
    if options.version is True:
        printVersion ()
        return
    if options.config is None:
        print >> sys.stderr, "Error requires config file see --help"
        sys.exit (1)
    try:
        parseConfig = CParser ()
        parseConfig.read (options.config)
        rbind = str (parseConfig.get ("watchyd", "web_bind"))
        rport = int (parseConfig.get ("watchyd", "web_port"))
        abind = str (parseConfig.get ("watchyd", "stats_bind"))
        aport = int (parseConfig.get ("watchyd", "stats_port"))
    except:
        print >> sys.stderr, "\nError Parsing config!"
        sys.exit (1)
    try:
        limit = int (parseConfig.get ("watchyd", "cache"))
    except:
        limit = 40 # default
    try:
        backends = str (parseConfig.get ("watchyd", "backends")).split ()
    except:
        backends = []
    finally:
        try:
            backends = [ BackendUtil.Backend (i, parseConfig) for i in backends ]
        except BackendUtil.BackendInitException:
            print >> sys.stderr, "Error intilizing backend %s" % sys.exc_info ()[1]
            sys.exit (-1)
    logging.config.fileConfig (options.config)
    if options.fork is True:
        pid = os.fork ()
        if pid == -1:
            print >> sys.stderr, "Error forking as daemon"
            sys.exit (1)
        elif pid == 0:
            os.setsid ()
            os.umask (0)
        else:
            print pid
            sys.exit (0)
    StatsServer.WatchyDServer (limit, backends, wbind=rbind, wport=rport,
                               ubind=abind, uport=aport).listen ()

if __name__ == "__main__":
    serverMain ()
