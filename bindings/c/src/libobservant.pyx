import StatsCore

from posix.unistd cimport pid_t

Daemon = None

cdef public int obs_attach_to_stats_daemon(const char *pid, const char *sock):
    global Daemon
    try:
        Daemon = StatsCore.attchToStatsDaemon(pid=pid, sock=sock)
        return 0
    except:
        return -1

cdef public int obs_watch_pid(const pid_t pid, const char *key):
    global Daemon
    if Daemon is None:
        return -1
    Daemon.postWatchPid(key.decode('utf-8'), pid)
    return 0

cdef public int obs_stop_watch_pid(const pid_t pid):
    global Daemon
    if Daemon is None:
        return -1
    Daemon.postStopWatchPid(pid)
    return 0

cdef public int obs_stop_watch_key(const char *key):
    global Daemon
    if Daemon is None:
        return -1
    Daemon.postStopWatchKey(key.decode('utf-8'))
    return 0

cdef public int obs_post_log_message(const char *key, const char *message):
    global Daemon
    if Daemon is None:
        return -1
    Daemon.postLogMessageForKey(key.decode('utf-8'), message.decode('utf-8'))
    return 0

cdef public void obs_detach_daemon():
    if Daemon:
        Daemon.close()
