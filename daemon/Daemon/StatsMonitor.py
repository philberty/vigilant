import psutil
import datetime
import platform


def get_host_stats(key):
    return {
        'key': key,
        'type': 'host',
        'payload': {
            'platform': platform.platform(),
            'hostname': platform.node(),
            'machine': platform.machine(),
            'version': platform.version(),
            'cores': psutil.cpu_count(),
            'cpu_stats': psutil.cpu_percent(interval=1, percpu=True),
            'usage': psutil.cpu_times_percent().user,
            'memory_total': psutil.virtual_memory().total,
            'memory_used': psutil.virtual_memory().used,
            'disk_total': psutil.disk_usage('/').total,
            'disk_free': psutil.disk_usage('/').used,
            'timestamp': datetime.datetime.now().isoformat(),
            'processes': len(psutil.pids())
        }
    }


def trim_string(string, max_length=128):
    buffer = ""
    length = len(string)
    for i in range(max_length):
        if i > length - 4:
            buffer += "..."
            break
        buffer += string[i]
    return buffer


def _stringify_string_list(data):
    retval = ""
    for i in data:
        retval += str(i)
    return trim_string(retval)


def get_stats_for_pid(pid):
    p = psutil.Process(pid)
    return {
        'pid': pid,
        'name': p.name(),
        'path': p.exe(),
        'cwd': p.cwd(),
        'cmdline': p.cmdline(),
        'status': p.status(),
        'user': p.username(),
        'threads': p.num_threads(),
        'fds': p.num_fds(),
        'files': _stringify_string_list(p.open_files()),
        'usage': p.cpu_percent(interval=1),
        'memory_percent': p.memory_percent(),
        'connections': _stringify_string_list(p.connections())
    }
