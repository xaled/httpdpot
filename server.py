#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl
import logging
from urllib.parse import urlencode
import hashlib
import os

logger = logging.getLogger(__name__)


def get_http_handler_class(response_text='', output_content=True, content_out_dir='./out', max_log_content=100,
                           max_out_content=10485760):
    handler_logger = logging.getLogger('requests')

    class HttpHandler(BaseHTTPRequestHandler):
        # def __getattr__(self, item):
        #     if item.startswith('do_'):
        #         method = item[3:]
        #
        #         def f():
        #             return self._handle_do_request(method)
        #
        #         return f
        #     return None

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
            handler_logger.info("%s %s %s %s" % (method, self.path,
                                                 urlencode(self.headers), urlencode(params)))

            # response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(response_text.encode('utf-8'))

    return HttpHandler


def run(server_class=HTTPServer, port=8443):
    server_address = ('', port)
    httpd = server_class(server_address, get_http_handler_class())
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile='./server.pem', server_side=True)
    logger.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
    finally:
        httpd.server_close()
        logger.info('Stopping httpd...\n')

def configure_logging(filepath):
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
                'maxBytes': 10485760,
                'backupCount': 5}
        },
        'formatters': {
            'file_formatter': {
                'format': '%(asctime)s %(message)s',
                'datefmt': '%Y-%m-%dT%H:%M:%S%z'
            }
        },
        'loggers': {
            '': {'level': 'WARNING', 'handlers': ['console_handler', 'file_handler']},
            '__main__': {'level': 'DEBUG'},
            'requests': {'level': 'INFO'}
        }
    }
    logging.config.dictConfig(config_dict)

def parse_args():
    import argparse
    # parser = argparse.ArgumentParser()
    #
    # parser.add_argument('-s', action='store', dest='simple_value',
    #                     help='Store a simple value')
    #
    # parser.add_argument('-c', action='store_const', dest='constant_value',
    #                     const='value-to-store',
    #                     help='Store a constant value')
    #
    # parser.add_argument('-t', action='store_true', default=False,
    #                     dest='boolean_switch',
    #                     help='Set a switch to true')
    # parser.add_argument('-f', action='store_false', default=False,
    #                     dest='boolean_switch',
    #                     help='Set a switch to false')
    #
    # parser.add_argument('-a', action='append', dest='collection',
    #                     default=[],
    #                     help='Add repeated values to a list',
    #                     )
    #
    # parser.add_argument('-A', action='append_const', dest='const_collection',
    #                     const='value-1-to-append',
    #                     default=[],
    #                     help='Add different values to list')
    # parser.add_argument('-B', action='append_const', dest='const_collection',
    #                     const='value-2-to-append',
    #                     help='Add different values to list')
    # args = parser.parse_args()
    return

if __name__ == "__main__":
    # os.makedirs('./logs')
    # os.makedirs('./out')

    args = parse_args()
    configure_logging('logs/requests.log')
    run()


