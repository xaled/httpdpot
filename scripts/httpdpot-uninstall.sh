#!/bin/bash

echo_and_run() { echo "$@" ; "$@" ; }

echo_and_run systemctl stop httpdpot
echo_and_run systemctl disable httpdpot
echo_and_run rm -Rf /opt/httpdpot
echo_and_run systemctl daemon-reload
echo_and_run systemctl reset-failed
