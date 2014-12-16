# Observant
[![MIT License](http://b.repl.ca/v1/License-MIT-red.png)](LICENSE)

Observant provides application driven, distributed stats/process/log monitoring.

##Setup

There are 3 Components for a full setup of Observant:

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

Scala DataStore uses sbt (requires jdk >= 7):

```bash
$ ./sbt # -jvm-debug 5005 for debugging
> container:start               # start the container
> ~ ;copy-resources;aux-compile # auto-reload on file changes
```

Flask Angularjs Dashbaord

```bash
$ bower install
$ ./dashboard.py -c etc/observant/observant.cfg
```

###Project Files
I use emacs and intellij and this project contains run configurations and setup for doing all development from intellij.

## Creators

**Philip Herron**

- <http://redbrain.co.uk>
- <https://twitter.com/redzor>
- <https://github.com/redbrain>

## Copyright and license

Code and documentation copyright 2014-2015 Philip Herron, Code released under [the MIT license](LICENSE). Docs released under Creative Commons.
