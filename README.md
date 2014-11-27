# ⛨ Observant ⛨

[![Daemon Build Status](https://travis-ci.org/redbrain/observant.svg?branch=master)](https://travis-ci.org/redbrain/observant)
[![DataStore Build Status](https://drone.io/github.com/redbrain/observant/status.png)](https://drone.io/github.com/redbrain/observant/latest)
[![MIT License](http://b.repl.ca/v1/License-MIT-red.png)](LICENSE)
[![Coverage Status](https://img.shields.io/coveralls/redbrain/observant.svg)](https://coveralls.io/r/redbrain/observant)

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
# check if it is running
$ python3 daemon.py -c etc/observant/observant.cfg --status
True

# kill the daemon gracefully
$ python3 daemon.py -c etc/observant/observant.cfg --kill

# Make sure it is dead
$ ./daemon.py -c etc/observant/observant.cfg --status
Daemon process not alive [/tmp/watchy.pid]

# Start the Daemon
$ ./daemon.py -c etc/observant/observant.cfg --start

# Make sure it is running
$ ./daemon.py -c etc/observant/observant.cfg --status
True
```

Scala DataStore uses sbt (requires jdk >= 7):

```bash
$ ./sbt
> container:start               # start the container
> ~ ;copy-resources;aux-compile # auto-reload on file changes
```

Nodejs Expressjs dashboard Front-end

```bash
$ brew install node
$ cd dashboard
$ npm install
$ bower install
$ node ./bin/www
```

###Project Files
I use emacs and intellij and this project contains run configurations and setup for doing all development from intellij.

## Creators

**Philip Herron**

- <http://redbrain.co.uk>
- <https://twitter.com/redzor>
- <https://github.com/redbrain>

## Copyright and license

Code and documentation copyright 2014 Philip Herron, Code released under [the MIT license](LICENSE). Docs released under Creative Commons.
