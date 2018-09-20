#!/bin/bash
ps aux | grep -ie "/opt/httpdpot/httpdpot/server.py" | awk '{print $2}' | xargs kill