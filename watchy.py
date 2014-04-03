#!/usr/bin/env python

import os
import sys
import logging
import optparse
import traceback

from WatchyServer import ServerUtil
from WatchyServer import StatsServer
from ConfigParser import SafeConfigParser

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
    parser.add_option ("-N", "--name", dest="name",
                       help="Logging name", default="WATCHY")
    parser.add_option ("-d", "--debug", dest="debug", action="store_true",
                       help="Verbose Debugging on of off", default=False)
    (options, args) = parser.parse_args ()
    if options.version is True:
        printVersion ()
        return
    if options.config is None:
        print >> sys.stderr, "Error requires config file see --help"
        sys.exit (1)
    try:
        parseConfig = SafeConfigParser ()
        parseConfig.read (options.config)
        rbind = str (parseConfig.get ("watchyd", "web_bind"))
        rport = int (parseConfig.get ("watchyd", "web_port"))
        abind = str (parseConfig.get ("watchyd", "stats_bind"))
        aport = int (parseConfig.get ("watchyd", "stats_port"))
    except:
        print >> sys.stderr, "\nError Parsing config!"
        sys.exit (1)
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
    form = '[' + options.name + '] %(levelname)s %(message)s'
    level = logging.DEBUG if options.debug else logging.INFO
    logging.basicConfig (filename = options.logfile, level = level, format = form,
                         datefmt = '%m/%d/%Y %I:%M:%S', filemode = 'w+')
    if options.debug is True:
        rootLogger = logging.getLogger ()
        consoleHandler = logging.StreamHandler ()
        formatter = logging.Formatter (form)
        consoleHandler.setFormatter (formatter)
        rootLogger.addHandler (consoleHandler)
    StatsServer.WatchyDServer (wbind=rbind, wport=rport,
                               ubind=abind, uport=aport,
                               debug=options.debug).listen ()

if __name__ == "__main__":
    serverMain ()
