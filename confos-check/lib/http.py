"""Serve a payload directory from the host to the guest (QEMU user-mode network: the host is 10.0.2.2).

The server listens on 127.0.0.1 only; QEMU user-mode networking delivers the guest's connections to 10.0.2.2
to the host's loopback. Every request is recorded in the evidence.
"""
import functools
import http.server
from pathlib import Path
import threading

from .common import utc

GUEST_HOST = '10.0.2.2'


class PayloadServer:
    def __init__(self, directory, evidence):
        self.directory = Path(directory)
        self.ev = evidence
        log = self.ev.dir / 'http-requests.log'

        class Handler(http.server.SimpleHTTPRequestHandler):
            def log_message(self, fmt, *args):
                with open(log, 'a') as f:
                    f.write(f'{utc()} {self.client_address[0]} {fmt % args}\n')

        handler = functools.partial(Handler, directory=str(self.directory))
        self.httpd = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
        self.port = self.httpd.server_address[1]
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)

    def __enter__(self):
        self.thread.start()
        self.ev.note(f'payload server for {self.directory.name} on 127.0.0.1:{self.port} '
                     f'(guest URL http://{GUEST_HOST}:{self.port}/)')
        return self

    def url(self, name):
        return f'http://{GUEST_HOST}:{self.port}/{name}'

    def __exit__(self, *exc):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.ev.note(f'payload server on port {self.port} stopped')
