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
$ sudo -E python setup.py install
```

## Usage

Firstly you should setup the server open /etc/watchy/watchy.cfg

```bash
[watchyd]
web_bind = 0.0.0.0     # address to bind to for web app
web_port = 7777        # port to serve the web app
stats_bind = localhost # stats aggregator bind
stats_port = 7878      # stats aggregator port
backends = none        # This is in progress to store stats
```

Now you can run the web app:

```bash
$ /usr/local/bin/watchy.py --help
Usage: watchy.py [options]

Options:
  -h, --help            show this help message and exit
  -v, --version         Print version
  -l LOGFILE, --logfile=LOGFILE
                        Ouput logfile
  -c CONFIG, --config=CONFIG
                        Config file location
  -F, --fork            Fork as daemon
  -N NAME, --name=NAME  Logging name
  -d, --debug           Verbose Debugging on of off

$ /usr/local/bin/watchy.py -F -N watchy1 -l ./watchy-server.log -c /etc/watchy/watchy.cfg
$ tail -f watchy-server.log 
[watchy1] INFO  * Running on http://0.0.0.0:7777/
[watchy1] INFO Starting StatsAggregator on localhost:7878
...
$ kill pid
```

Now you should be able to point your browser to http://localhost:7777, this is
a python flask web application. A /etc/init.d script would be nice here,
and a way to run it via nginx or apache etc for a more real setup.

Sending stats can be done via:

```bash
$ /opt/watchy/bin/watcher -k `hostname` -b localhost -p 7878 process1:<pid> process2:<pid>
```

Or you can tail a log:

```bash
$ tail -f /var/log/syslog | /opt/watchy/bin/wtail -k syslog -p 7878 -b localhost
```

##Platform Support

Currently the python server should run on anywhere that has flask and python 2.7,
but the library has only been ported to darwin (Mac OSX) and linux (Ubuntu/RedHat).

*BSD and Solaris support is eventually going to pop along.

## RestApi

The Flask web app exposes a very simple rest api, a web socket api is planned for
real time stats per node. All rest calls are json no xml support.

  * http://host:port/api/{process/hosts/logs}/keys - Get all node key names
  * http://host:port/api/{process/hosts/logs}/data/<node-name>, Get the current session raw data
  * http://host:port/api/{process/hosts}/graph/<node-name>, Get the current session graph data

The web socket api is going to be very useful here and a zeromq a rabbit amqp backend too.
