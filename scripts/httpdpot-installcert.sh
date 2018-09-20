#!/bin/bash
openssl genrsa  -out /opt/httpdpot/server.key 2048
openssl req -new -key /opt/httpdpot/server.key -out /opt/httpdpot/server.csr
openssl x509 -req -days 1024 -in /opt/httpdpot/server.csr -signkey /opt/httpdpot/server.key -out /opt/httpdpot/server.crt
cat /opt/httpdpot/server.crt /opt/httpdpot/server.key > /opt/httpdpot/server.pem