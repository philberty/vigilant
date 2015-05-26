#!/usr/bin/env bash

cd $(dirname ${BASH_SOURCE[0]})
nginx -s stop

set -e
nginx -p `pwd` -c ./etc/nginx/nginx.cfg -t
nginx -p `pwd` -c ./etc/nginx/nginx.cfg
uwsgi -s /tmp/uwsgi.sock -w dashboard:app
