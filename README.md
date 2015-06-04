# Vigilant
[![Build Status](http://jenkins.vigilantlabs.co.uk/buildStatus/icon?job=Vigilant)](http://jenkins.vigilantlabs.co.uk/job/Vigilant/)
[![MIT License](http://b.repl.ca/v1/License-MIT-red.png)](LICENSE)

Vigilant provides application driven stats monitoring. When you integrate your application
with the Daemon bindings/library every time your application starts a daemon is created and
all other processes will attach to this daemon sending watch/log/alert messages which in turn
are delivered to a datastore. Because your own applications know their pid (od.getpid()) you no
longer need to manage your monitoring with runner scripts.

## Screenshots

![Overview](/screenshots/overview.png "Overview")
![Real-Time](/screenshots/real-time.png "Real-Time")

## Tutorial

Detailed Setup tutorial can be found here https://github.com/redbrain/vigilant/wiki/QuickSetup

## Deps

You will require Open/Oracle JDK >= 1.7, Python >= 3.4, Bower.

Mac OSX
```bash
# download orcale jdk.
$ brew install python3 npm
$ npm install -g bower
```

Ubuntu

```bash
$ sudo apt-get install default-jdk python3.4 nodejs
$ npm install -g bower
```

### Setup Daemon Agent

Currently daemon2 is a WIP and not ready but Daemon is proof of concept. It requires python >= 3.4

```bash
$ cd daemon
$ sudo pip3 install -r requirements.txt
$ ./daemon.py -c etc/vigilant/vigilant.json --start
```

Editing the vigilant.json declares where data is sent and the protocol. Currently only udp is supported by the datastore.
And i aim to keep using UDP as the main protocol. And use ack's for alerts/triggers from code to ensure they are sent.

Using --stop or --status will stop the daemon or show status of what the agent is watching and sending the data to respectively.

### Setup Datastore

Once an agent is running the data needs to be recieved. The datastore will accept all the data and provide functionality over it.
Written in Scala requires jdk >= 1.7.

```bash
$ cd datastore
$ bower install
$ cd etc/vigilant
$ export VIGILANT_HOME=`pwd`
$ cd -
$ ./sbt
> compile
> test
> container:start
```

Currently deploying the .war onto jetty or tomcat runner the websocket api doesnt work. Editing the vigilant configuration:

```javascript
    "transport": {
        "type": "udp",
        "host": "localhost",
        "port": 8080
    },

    "triggers": {
      "notification_threshold": 120 // How often should notifications be send if data continues to activate triggers. To stop notification spam.
    },

    "database": {
      "jdbc": "jdbc:h2:./vigilant" // FIXME
    },

    "twillo": {
        "account_sid": "", # twillo details to enable twillo notifications
        "auth_token": "",
        "from": ""
    },

    "email": {
      "smtp_server": "localhost", # email details doesnt handle tls/ssl like gmail.com
      "from": "someone@email.com"
    }
}
```

View swagger api documentation: http://localhost:8080/api and use /api-doc as the location to the documenation.

### Front-end

The front-end webapp is a seperate project abstracting datastores.

```bash
$ sudo pip3 install -r requirements.txt
$ bower install
$ ./dashboard.py
```

Go to http://localhost:5000/#/dashboard?store=http://localhost:8080

## Daemon

The proof-of-concept daemon, this is being re-written in C/C++ to increase portability and
simplicity of language bindings. Currently because this is written in Python3 Node bindings require
python3 to be installed which isn't very elegant.

## Daemon 2

This is a WIP new Daemon written in C/C++ to increase the protability and simplicity of adding simple dependancies.

## Datastore

The scala data-store listens for the real-time data and in turn provides a rest-api for working with
this. The api is fully documented at http://localhost:8080/api using swagger. The web-socket api isn't
supported by swagger but it is there.

## Front-end

This is the current front-end it needs more work but its working quite well for now. It simply uses the
data-store rest-api to access the monitoring data.
