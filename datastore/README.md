# Vigilant DataStore
[![Build Status](http://jenkins.vigilantlabs.co.uk/buildStatus/icon?job=Datastore)](http://jenkins.vigilantlabs.co.uk/job/Datastore/)

Real-time datastore - 

##Setup

Scala DataStore uses sbt (requires jdk >= 7):

```bash
$ ./sbt # -jvm-debug 5005 for debugging
> container:start               # start the container
> ~ ;copy-resources;aux-compile # auto-reload on file changes
```

```bash
# run standalone jetty container
$ ./jetty.sh
```
