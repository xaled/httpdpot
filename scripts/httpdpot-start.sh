 #!/bin/bash
/opt/httpdpot/httpdpot/server.py -p 7547 -L /opt/httpdpot/logs/ -O /opt/httpdpot/out/  &
/opt/httpdpot/httpdpot/server.py -p 80 -L /opt/httpdpot/logs/ -O /opt/httpdpot/out/  &
/opt/httpdpot/httpdpot/server.py -p 8080 -L /opt/httpdpot/logs/ -O /opt/httpdpot/out/  &
/opt/httpdpot/httpdpot/server.py -s 443  -c /opt/httpdpot/server.pem -L /opt/httpdpot/logs/ -O /opt/httpdpot/out/  &
/opt/httpdpot/httpdpot/server.py -s 8443 -L /opt/httpdpot/logs/ -O /opt/httpdpot/out/  &
