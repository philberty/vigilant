#Observant

Observant provides application driven, distributed stats/process/log monitoring.

##Setup

There are 3 Components for a full setup of Observant:

Stats Daemon (requires python3):

```python
$ sudo pip3 install -r requirements.txt
$ python3 setup.py install
$ python3 daemon.py -c etc/observant/observant.cfg --status
True
$ python3 daemon.py -c etc/observant/observant.cfg --kill
$ ./daemon.py -c etc/observant/observant.cfg --status
Daemon process not alive [/tmp/watchy.pid]
$ ./daemon.py -c etc/observant/observant.cfg --start
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
$ cd dashboard
$ npm install
$ bower install
$ node ./bin/www
```
