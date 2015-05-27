# Vigilant
[![MIT License](http://b.repl.ca/v1/License-MIT-red.png)](LICENSE)

Vigilant provides application driven stats monitoring. When you integrate your application
with the Daemon bindings/library every time your application starts a daemon is created and
all other processes will attach to this daemon sending watch/log/alert messages which in turn
are delivered to a datastore. Because your own applications know their pid (od.getpid()) you no
longer need to manage your monitoring with runner scripts.


## Daemon

The proof-of-concept daemon, this is being re-written in C/C++ to increase portability and
simplicity of language bindings. Currently because this is written in Python3 Node bindings require
python3 to be installed which isn't very elegant.

## Datastore

The scala data-store listens for the real-time data and in turn provides a rest-api for working with
this. The api is fully documented at http://localhost:8080/api using swagger. The web-socket api isn't
supported by swagger but it is there.

## Front-end

This is the current front-end it needs more work but its working quite well for now. It simply uses the
data-store rest-api to access the monitoring data.
