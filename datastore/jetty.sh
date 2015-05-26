#!/usr/bin/env bash
set -e

./sbt -mem 128 test package

export VIGILANT_HOME=`pwd`/etc/vigilant/

java -Xms128m -Xmx128m \
    -jar ./libexec/jetty-runner-9.2.2.v20140723.jar \
    --port 9090 \
    ./target/scala-2.11/vigilant_2.11-0.2.0-SNAPSHOT.war
