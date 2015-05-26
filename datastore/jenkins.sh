#!/usr/bin/env bash
set -e

bower install
./sbt -mem 256 compile package test
