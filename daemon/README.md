# Vigilant Daemon

This is the user agent daemon required to aggregate stats on each host for n-applications

##Setup

Stats Daemon (requires python3):

```python
$ brew install python3
$ pip3 install -r requirements.txt
$ python3 setup.py install
```

Simple Daemon.py manager usage

```python
# Start the Daemon
$ ./daemon.py -c etc/vigilant/vigilant.json --start

# Make sure it is running
$ ./daemon.py -c etc/vigilant/vigilant.json --status
{
    "transport": "UDP Transport localhost:8080",
    "watching": {
        "Philips-MacBook-Pro.local.StatsDaemon": 914
    },
    "host": "Philips-MacBook-Pro.local"
}
True

# kill the daemon gracefully
$ ./daemon.py -c etc/vigilant/vigilant.json --kill
```


## Configuration

The configuration is meant to be as simple as possible.

 * Transport Section defines the data-store location and protocol type currently only udp is supported by the data-store
 * Daemon Section defines the lock and unix-socket path to use for the daemon.

