import os
import sys
import argparse

import tornado.ioloop
import tornado.web


class Handler(tornado.web.StaticFileHandler):

    def parse_url_path(self, url_path):
        if not url_path or url_path.endswith('/'):
            url_path = url_path + 'index.html'
        return url_path


def setup_app(prefix=''):
    if prefix:
        path = '/' + prefix + '/(.*)'
    else:
        path = '/(.*)'

    application = tornado.web.Application([
        (path, Handler, {'path': os.getcwd()}),
    ], debug=True)

    return application


def start_server(prefix='', port=8000):
    app = setup_app(prefix)
    app.listen(port)
    tornado.ioloop.IOLoop.instance().start()


def parse_args(args=None):
    parser = argparse.ArgumentParser(description=(
        'Start a Tornado server to serve static files out of a '
        'given directory.'))
    parser.add_argument(
        '-f', '--prefix', type=str, default='',
        help='A prefix to add to the location from which pages are served.')
    parser.add_argument(
        '-p', '--port', type=int, default=8000,
        help='Port on which to run server.')
    parser.add_argument(
        '-d', '--directory', help='Directory from which to serve files.', default='.')
    return parser.parse_args(args)


def main(args=None):
    args = parse_args(args)
    os.chdir(args.directory)
    print('Starting server on port {}...'.format(args.port))
    start_server(prefix=args.prefix, port=args.port)


if __name__ == '__main__':
    sys.exit(main())
