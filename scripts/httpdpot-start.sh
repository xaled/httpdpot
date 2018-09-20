 #!/bin/bash
/opt/httpdpot/repo/server.py -p 7547 -L /opt/httpdpot/log/ -O /opt/httpdpot/out/  &
/opt/httpdpot/repo/server.py -p 80 -L /opt/httpdpot/log/ -O /opt/httpdpot/out/  &
/opt/httpdpot/repo/server.py -p 8080 -L /opt/httpdpot/log/ -O /opt/httpdpot/out/  &
/opt/httpdpot/repo/server.py -s -p 443  -c /opt/httpdpot/server.pem -L /opt/httpdpot/log/ -O /opt/httpdpot/out/  &
/opt/httpdpot/repo/server.py -s -p 8443 -c /opt/httpdpot/server.pem -L /opt/httpdpot/log/ -O /opt/httpdpot/out/  &
