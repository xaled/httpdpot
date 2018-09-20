#!/bin/bash
ps aux | grep -ie "/opt/httpdpot/repo/server.py" | awk '{print $2}' | xargs kill