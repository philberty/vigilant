import os
from . import StatsDaemon

def attchToStatsDaemon(pid='/tmp/watchy.pid', sock='/tmp/watchy.sock'):
    return StatsDaemon.ClientDaemonConnection(pid=pid, sock=sock)

def createStatsDaemon(key, transport, pid='/tmp/watchy.pid', sock='/tmp/watchy.sock'):
    daemon = StatsDaemon.StatServerDaemon(key, transport, os.getpid(), pid=pid, sock=sock)
    StatsDaemon.forkStatsDaemon(daemon, lock=pid)

def attachOrCreateStatsDaemon(key, transport, pid='/tmp/watchy.pid', sock='/tmp/watchy.sock'):
    createStatsDaemon(key, transport, pid=pid, sock=sock)
    return StatsDaemon.ClientDaemonConnection(pid=pid, sock=sock)
