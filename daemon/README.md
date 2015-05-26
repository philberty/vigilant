# Vigilant Daemon
[![MIT License](http://b.repl.ca/v1/License-MIT-red.png)](LICENSE)
[![Build Status](https://travis-ci.org/VigilantLabs/vigilant-daemon.svg)](https://travis-ci.org/VigilantLabs/vigilant-daemon)

This is the user agent daemon required to aggregate stats on each host for n-applications

##Setup

Stats Daemon (requires python3):

```python
$ brew install python3
$ sudo pip3 install -r requirements.txt
$ python3 setup.py install
```

Simple Daemon.py manager usage

```python
# Start the Daemon
$ ./daemon.py -c etc/observant/observant.cfg --start

# Make sure it is running
$ ./daemon.py -c etc/observant/observant.cfg --status
{
    "transport": "UDP Transport localhost:8080",
    "watching": {
        "Philips-MacBook-Pro.local.StatsDaemon": 914
    },
    "host": "Philips-MacBook-Pro.local"
}
True

# kill the daemon gracefully
$ ./daemon.py -c etc/observant/observant.cfg --kill
```

## Creators

**Philip Herron**

- <http://redbrain.co.uk>
- <https://twitter.com/redzor>
- <https://github.com/redbrain>

## Copyright and license

Code and documentation copyright 2014-2015 Philip Herron, Code released under [the MIT license](LICENSE). Docs released under Creative Commons.
