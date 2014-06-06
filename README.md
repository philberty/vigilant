# Watchy

[![Build Status](https://travis-ci.org/redbrain/watchy.svg?branch=master)](https://travis-ci.org/redbrain/watchy)

Inspried by StatsD, an embedable library that will automatically
watch your process from a single function call and will stop when
your process stops. No need to externally start a process to watch
and send stats. Its efficient and simple and easy to use is 100% the
goal of this project.

## Compilation

To compile and setup the system:

```bash
$ autoreconf --force --install
$ ./configure CC=clang/gcc CFLAGS="-g -O2 -Wall" --prefix=/opt/watchy
$ make
$ make install
```

To compile using the library use:

```bash
$ export PKG_CONFIG_PATH=/opt/watchy/lib/pkgconfig:$PKG_CONFIG_PATH
$ pkg-config watchy --cflags --libs
```

Now the shared library is installed

```bash
$ sudo pip install -r requirements.txt
$ # the python setup.py will create the cython module but it requires pkg-config watchy to work
$ python setup.py build
$ # sudo -E so it will export PKG_CONFIG_PATH
$ sudo -E python setup.py install --prefix=/opt/watchy
```

## Usage

Firstly you should setup the server an example config should be in /etc/watchy/example-watchy.cfg

```bash
[watchyd]
web_bind = 0.0.0.0     # address to bind to for web app
web_port = 7777        # port to serve the web app
stats_bind = localhost # stats aggregator bind
stats_port = 7878      # stats aggregator port
```

This is the barebones configuration, the web bind and port is required for the web dashboard the stats bind/port is for the stats aggregation process. Clients the watchydaemon send data to this not the dashboard.

Now you can run the web app:

```bash
$ /usr/local/bin/watchy.py --help
Usage: watchy.py [options]

Options:
  -h, --help            show this help message and exit
  -v, --version         Print version
  -c CONFIG, --config=CONFIG
                        Config file location
  -F, --fork            Fork as daemon

```

You can run this server via:

```bash
$ /usr/local/bin/watchy.py -c /etc/watchy/example-watchy.cfg 
WATCHY INFO - Starting StatsAggregator on 0.0.0.0:7878
WATCHY INFO - Starting Async Backend handler
WATCHY INFO - WSGIServer:[gevent] starting http://0.0.0.0:8787/
...
```

You should be able to point your browser to http://localhost:8787, you can fork as a daemon and change your logging config in the config file as per pythong logging.config.

You can send stats up many ways but the easiest is:

```bash
$ /opt/watchy/bin/watcher -k hostname -b localhost -p 7878 process1:<pid> process2:<pid>
```

Or you can tail a log:

```bash
$ tail -f /var/log/syslog | /opt/watchy/bin/wtail -k syslog -p 7878 -b localhost
```

The web app should automatically update and you should see things going off if not look at the log and see if it is getting any stats.

##Backends

Currently the mongodb backend is the only working backend to enable it specify in the config:

```ini
[watchyd]
backends = mongo

[mongo]
type = mongodb
uri = mongodb://localhost:27017

```

You simple specify the URI to your mongo instance this works via: pymongo MongoClient (uri). Zeromq, RabbitMq, Websockets and Ganglia are currently under development.

##Platform Support

Currently the python server should run on anywhere that has flask and python 2.7,
but the library has only been ported to darwin (Mac OSX) and linux (Ubuntu/RedHat).

*BSD and Solaris support is eventually going to pop along.

## RestApi

The Flask web app exposes a very simple rest api, a web socket api is planned for
real time stats per node. All rest calls are json no xml support.

  * http://host:port/api/{process/hosts/logs}/keys - Get all node key names
  * http://host:port/api/{process/hosts/logs}/data/<node-name>, Get the current session raw data

The web socket api is going to be very useful here and a zeromq a rabbit amqp backend too.
