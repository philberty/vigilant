import os

import Daemon

_Daemon = None
_PROC_NAME = None

cdef public int obs_attach_to_stats_daemon(const char *key, const char *pid, const char *sock):
    global _Daemon, _PROC_NAME
    _PROC_NAME = key.decode('utf-8')
    try:
        _Daemon = Daemon.attach_to_daemon(pid=pid, sock=sock)
        _Daemon.post_watch_pid(_PROC_NAME, os.getpid())
        return 0
    except:
        import sys
        print(sys.exc_info()[1])
        return -1

cdef public int obs_post_message(const char *message):
    global _Daemon, _PROC_NAME
    if _Daemon is None:
        return -1
    _Daemon.post_log_message_for_key(message.decode('utf-8'), proc=_PROC_NAME)
    return 0

cdef public void obs_detach_daemon():
    global _Daemon
    if _Daemon:
        _Daemon.close()
