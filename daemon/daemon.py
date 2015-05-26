#!/usr/bin/env python3

import os
import sys
import json
import optparse

import Daemon
from Daemon import DaemonIPC
from Daemon import Transports


def is_daemon_running(lock):
    return DaemonIPC.is_pid_alive(DaemonIPC.get_pid_from_lock(lock))


def get_daemon_status(lock, sock):
    try:
        client = Daemon.attach_to_daemon(pid=lock, sock=sock)
        mess = client.post_status_request()
        client.close()
        return mess
    except:
        return sys.exc_info()[1]
    

def stop_daemon(lock, sock):
    if is_daemon_running(lock):
        client = Daemon.attach_to_daemon(pid=lock, sock=sock)
        client.post_stop_daemon()
        client.close()
        try:
            os.waitpid(DaemonIPC.get_pid_from_lock(lock), 0)
        except:
            pass


def get_transport_from_config(config):
    transport_section = config['transport']
    transport_type = transport_section['type']
    if transport_type == 'udp':
        return Transports.UDPStatsTransport(host=transport_section['host'], port=transport_section['port'])
    elif transport_type == 'tcp':
        return Transports.TCPStatsTransport(host=transport_section['host'], port=transport_section['port'])
    else:
        raise Exception('Invalid transport in configuration')
    

def get_daemon_connection(config):
    lock = config['daemon']['lock']
    sock = config['daemon']['sock']
    transport = get_transport_from_config(config)
    return Daemon.attach_or_create_daemon(transport, pid=lock, sock=sock)


def start_daemon(config):
    client = get_daemon_connection(config)
    client.close()


def watch_pid(config, key, pid):
    lock = config['daemon']['lock']
    if not is_daemon_running(lock):
        sys.exit("ERROR: Daemon not running")
    if not DaemonIPC.is_pid_alive(pid):
        sys.exit("ERROR: pid [%i] does not exist" % pid)
    client = get_daemon_connection(config)
    client.post_watch_pid(key, pid)
    client.close()


def log_message(message, lock, sock):
    try:
        client = Daemon.attach_to_daemon(pid=lock, sock=sock)
        client.post_log_message_for_key(message)
        client.close()
    except:
        return sys.exc_info()[1]


def daemon():
    parser = optparse.OptionParser()
    parser.add_option("-c", dest="config", help="Config file location", default=None)
    parser.add_option("--status", dest="status", help="Is daemon running", default=False, action="store_true")
    parser.add_option("--start", dest="start", help="Start Daemon with config", default=False, action="store_true")
    parser.add_option("--stop", dest="stop", help="Kill stats daemon", default=False, action="store_true")
    parser.add_option('--watch', dest='watch', default=None, help="Watch specified pid key:pid as argument")
    parser.add_option('--log', dest='log', default=None, help="Post log message")
    options, _ = parser.parse_args()
    if options.config is None:
        sys.exit('You must specify a configuration file, see --help')
    config = None
    with open(options.config) as fd:
        config = json.load(fd)
    lock = config['daemon']['lock']
    sock = config['daemon']['sock']
    if options.status:
        print(get_daemon_status(lock, sock))
    if options.stop:
        stop_daemon(lock, sock)
    if options.start:
        start_daemon(config)
    if options.log:
        log_message(options.log, lock, sock)
    if options.watch:
        split = options.watch.split(':')
        if len(split) != 2:
            sys.exit('ERROR: Invalid watch argument [%s] needs to be key:pid' % options.watch)
        watch_pid(config, split[0], int(split[1]))


if __name__ == "__main__":
    daemon()
