import os
from . import StatsDaemon

def attchToStatsDaemon(pid='/tmp/watchy.pid', sock='/tmp/watchy.sock'):
    return StatsDaemon.ClientDaemonConnection(pid=pid, sock=sock)

def createStatsDaemon(transport, pid='/tmp/watchy.pid', sock='/tmp/watchy.sock'):
    daemon = StatsDaemon.StatServerDaemon(transport, os.getpid(), pid=pid, sock=sock)
    StatsDaemon.forkStatsDaemon(daemon, lock=pid)

def attachOrCreateStatsDaemon(transport, pid='/tmp/watchy.pid', sock='/tmp/watchy.sock'):
    createStatsDaemon(transport, pid=pid, sock=sock)
    return StatsDaemon.ClientDaemonConnection(pid=pid, sock=sock)
