import os

from . import Daemon
from . import DaemonIPC


def attach_to_daemon(pid='/tmp/vigilant.pid', sock='/tmp/vigilant.sock'):
    """
    Attach to existing daemon.

    :param pid: lock file default /tmp/observant.pid
    :param sock: unix socket path default /tmp/observant.sock
    :return: returns the StatsCore.StatsDaemon.ClientDaemonConnection
    """
    return DaemonIPC.ClientConnection(pid, sock)


def create_daemon(transport, pid='/tmp/vigilant.pid', sock='/tmp/vigilant.sock'):
    """
    Create and fork a new Stats Daemon.

    :param transport: The transport for the daemon to use
    :param pid: the pid lock file to use
    :param sock: the unix socket path to listen on
    """
    from socket import gethostname
    daemon = Daemon.StatsDaemon(gethostname(), transport, os.getpid(), pid, sock)
    DaemonIPC.fork_daemon(daemon, lock=pid)


def attach_or_create_daemon(transport, pid='/tmp/vigilant.pid', sock='/tmp/vigilant.sock'):
    """
    Attach to the system daemon or create it.

    :param transport: The transport object for the daemon to server
    :param pid: The pid lock file for the daemon
    :param sock: The socket path to communicate on
    :return: StatsCore.StatsDaemon.ClientDaemonConnection object or Exception
    """
    if DaemonIPC.is_pid_alive(DaemonIPC.get_pid_from_lock(pid)):
        return attach_to_daemon(pid=pid, sock=sock)
    else:
        create_daemon(transport, pid=pid, sock=sock)
        return attach_to_daemon(pid=pid, sock=sock)
