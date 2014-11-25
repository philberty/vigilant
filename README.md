#Observant

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
