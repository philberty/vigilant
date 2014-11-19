import os

from . import StatsDaemon
from . import StatsAsyncCore

def attchToStatsDaemon(pid='/tmp/watchy.pid', sock='/tmp/watchy.sock'):
    """

    :param pid:
    :param sock:
    :return:
    """
    return StatsDaemon.ClientDaemonConnection(pid=pid, sock=sock)

def createStatsDaemon(key, transport, pid='/tmp/watchy.pid', sock='/tmp/watchy.sock'):
    """

    :param key:
    :param transport:
    :param pid:
    :param sock:
    """
    daemon = StatsAsyncCore.StatServerDaemon(key, transport, os.getpid(), pid=pid, sock=sock)
    StatsDaemon.forkStatsDaemon(daemon, lock=pid)

def attachOrCreateStatsDaemon(key, transport, pid='/tmp/watchy.pid', sock='/tmp/watchy.sock'):
    """
    Attach to the system daemon or create it.

    :param key: The key name for the system, usualy the hostname of the system
    :param transport: The transport object for the daemon to server
    :param pid: The pid lock file for the daemon
    :param sock: The socket path to communicate on
    :return: StatsCore.StatsDaemon.ClientDaemonConnection object or Exception
    """
    createStatsDaemon(key, transport, pid=pid, sock=sock)
    return attchToStatsDaemon(pid=pid, sock=sock)
