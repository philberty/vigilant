# DataStore

This is the realtime datastore, providing a rest-api to access all data and add triggers.

##Setup

Scala DataStore uses sbt (requires jdk >= 7):

```bash
$ cd ./etc/vigilant
$ export VIGILANT_HOME=`pwd`
$ cd -

$ ./sbt # -jvm-debug 5005 for debugging
> container:start               # start the container
> ~ ;copy-resources;aux-compile # auto-reload on file changes
```

Standalone from sbt:

```bash
# run standalone jetty container - The websocket api fails using this currently.
$ ./jetty.sh
```

## Configuration

Currently vigilant supports twillo as a notification service. Stub configuration is already
in [vigilant.json](./etc/vigilant/vigilant.json).

## Memory usage

I spent alot of time making this run on a very low memory machines and it can go lower but its
perfectly reasonable to run ./sbt -mem 128 to be enough for this.
