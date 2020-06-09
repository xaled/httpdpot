# httpdpot
Simple Python HTTP Honeypot

## Usage examples:
* Start a honeypot listening to port 80:
  * `./server.py -p 80` 
* Start an HTTPS honeypot using an SSL certificate:
  * `./server.py -s -p 443  -c server.pem`
* Change where requests and logs are stored:
  * `./server.py -p 80`
* Other options:
  * `./server.py --help`

## Installation:
### Debian/Ubuntu:
`./scripts/httpdpot-install.sh`
