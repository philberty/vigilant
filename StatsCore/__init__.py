import os

from . import StatsDaemon
from . import StatsAsyncCore

def attchToStatsDaemon(pid='/tmp/observant.pid', sock='/tmp/observant.sock'):
    """
    Attach to existing daemon.

    :param pid: lock file default /tmp/observant.pid
    :param sock: unix socket path default /tmp/observant.sock
    :return: returns the StatsCore.StatsDaemon.ClientDaemonConnection
    """
    return StatsDaemon.ClientDaemonConnection(pid=pid, sock=sock)

def createStatsDaemon(transport, pid='/tmp/observant.pid', sock='/tmp/observant.sock'):
    """
    Create and fork a new Stats Daemon.

    :param transport: The transport for the daemon to use
    :param pid: the pid lock file to use
    :param sock: the unix socket path to listen on
    """
    from socket import gethostname
    daemon = StatsAsyncCore.StatServerDaemon(gethostname(), transport, os.getpid(), pid=pid, sock=sock)
    StatsDaemon.forkStatsDaemon(daemon, lock=pid)

def attachOrCreateStatsDaemon(transport, pid='/tmp/observant.pid', sock='/tmp/observant.sock'):
    """
    Attach to the system daemon or create it.

    :param transport: The transport object for the daemon to server
    :param pid: The pid lock file for the daemon
    :param sock: The socket path to communicate on
    :return: StatsCore.StatsDaemon.ClientDaemonConnection object or Exception
    """
    if StatsDaemon.isPidAlive(StatsDaemon.getPidFromLockFile(pid)):
        return attchToStatsDaemon(pid=pid, sock=sock)
    else:
        createStatsDaemon(transport, pid=pid, sock=sock)
        return attchToStatsDaemon(pid=pid, sock=sock)
