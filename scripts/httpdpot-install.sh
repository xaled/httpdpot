#!/bin/bash

echo_and_run() { echo "$@" ; "$@" ; }

echo_and_run mkdir /opt/httpdpot &&
echo_and_run mkdir /opt/httpdpot/repo  &&
echo_and_run mkdir -p /opt/httpdpot/{log,out}  &&
echo_and_run git clone https://github.com/xaled/httpdpot /opt/httpdpot/repo &&
echo_and_run cp -R /opt/httpdpot/repo/scripts  /opt/httpdpot/ &&
echo_and_run /opt/httpdpot/scripts/httpdpot.enable.sh