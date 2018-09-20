#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl
import logging
from urllib.parse import urlencode
import hashlib
import os

logger = logging.getLogger(__name__)


def get_http_handler_class(response_text='', output_content=True, content_out_dir='./out', max_log_content=100,
                           max_out_content=10485760, server_url='server'):
    handler_logger = logging.getLogger('requests')

    class HttpHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            return self._handle_do_request('GET')

        def do_HEAD(self):
            return self._handle_do_request('HEAD')

        def do_POST(self):
            return self._handle_do_request('POST')

        def do_PUT(self):
            return self._handle_do_request('PUT')

        def do_DELETE(self):
            return self._handle_do_request('DELETE')

        def do_TRACE(self):
            return self._handle_do_request('TRACE')

        def do_OPTIONS(self):
            return self._handle_do_request('OPTIONS')

        def do_CONNECT(self):
            return self._handle_do_request('CONNECT')

        def do_PATCH(self):
            return self._handle_do_request('PATCH')

        def _handle_do_request(self, method):
            # content
            try:
                content_length = int(self.headers['Content-Length'])
            except:
                content_length = 0
            params = {'content_length': content_length}

            if 0 < content_length < max_log_content:
                params['content'] = self.rfile.read(content_length).decode(errors='replace')
            elif 0 < content_length < max_out_content and output_content:
                filepath = None
                try:
                    data = self.rfile.read(content_length)
                    filename = hashlib.md5(data).hexdigest() + '-' + str(content_length) + '.out'
                    params['filename'] = filename
                    filepath = os.path.join(content_out_dir, filename)

                    if not os.path.exists(filepath):
                        out_file = open(filepath, "wb")
                        out_file.write(data)
                        out_file.close()

                except Exception as e:
                    logger.error('Error saving HTTP request content to filepath: %s', filepath, exc_info=True)

            # log
            handler_logger.info("%s %s %s %s %s %s %s" % (self.client_address[0], self.client_address[1], server_url,
                                                          method, self.path, urlencode(self.headers), urlencode(params)))

            # response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(response_text.encode('utf-8'))

    return HttpHandler


def run(args):
    server_class = HTTPServer
    url = 'http%s://127.0.0.1:%d' % ('s' if args.ssl else '', args.port)
    server_url = 'http%s://0.0.0.0:%d' % ('s' if args.ssl else '', args.port)

    handler_class = get_http_handler_class(response_text=args.response_text,
                                           output_content=args.output_content,
                                           content_out_dir=args.out_dir,
                                           max_log_content=args.max_loggable_content_size,
                                           max_out_content=args.max_out_content_size,
                                           server_url=server_url
                                           )
    server_address = ('', args.port)
    httpd = server_class(server_address, handler_class)
    if args.ssl:
        httpd.socket = ssl.wrap_socket(httpd.socket, certfile=args.ssl_cert, server_side=True)
    logger.info('Starting httpd %s...', url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
    finally:
        httpd.server_close()
        logger.info('Stopping httpd...')


def configure_logging(args):
    filepath = os.path.join(args.log_dir, args.log_filename)
    import logging.config
    config_dict = {
        'version': 1,
        'handlers': {
            'console_handler': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'file_formatter'
            },
            'file_handler': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'DEBUG',
                'formatter': 'file_formatter',
                'filename': filepath,
                'mode': 'a',
                'maxBytes': args.log_file_max_bytes,
                'backupCount': args.log_file_backup_count}
        },
        'formatters': {
            'file_formatter': {
                'format': '%(asctime)s %(message)s',
                'datefmt': '%Y-%m-%dT%H:%M:%S%z'
            }
        },
        'loggers': {
            '': {'level': 'WARNING', 'handlers': ['console_handler']},
            '__main__': {'level': 'DEBUG'},
            'requests': {'level': 'INFO', 'handlers': ['console_handler', 'file_handler']}
        }
    }
    logging.config.dictConfig(config_dict)


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--port', action='store', type=int, default=None, help='server port')
    # parser.add_argument('-b', '--bind-address', action='store', default='', help='server bind address')
    parser.add_argument('-c', '--ssl-cert', action='store', default='./server.pem', help='SSL Certificate')
    parser.add_argument('-s', '--ssl', action='store_true', help='use HTTPS instead of HTTP')
    parser.add_argument('-L', '--log-dir', action='store', default='./logs', help="Log file dir")
    parser.add_argument('-O', '--out-dir', action='store', default='./out', help="Requests content output destination")
    parser.add_argument('--log-filename', action='store', default=None, help="Log file name")
    parser.add_argument('--do-not-output-content', dest="output_content", action='store_false', help="Do not output requests content")
    parser.add_argument('--max-loggable-content-size', action='store', type=int, default=100, help="Maximum loggable content in size")
    parser.add_argument('--max-out-content-size', action='store', type=int, default=10485760, help="Maximum output content in size")
    parser.add_argument('--response-text', action='store', default='')
    parser.add_argument('--log-file-max-bytes', action='store', type=int, default=10485760)
    parser.add_argument('--log-file-backup-count', action='store', type=int, default=5)

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    # os.makedirs('./logs')
    # os.makedirs('./out')

    args = parse_args()
    if not os.path.exists(args.log_dir):
        os.makedirs(args.log_dir)
    if args.output_content and not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)
    if args.port is None:
        args.port = 8443 if args.ssl else 8080
    if args.log_filename is None:
        args.log_filename = 'requests_%s_%d.log' % ('https' if args.ssl else 'http', args.port)
    configure_logging(args)
    run(args)


