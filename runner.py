# -*- coding: utf-8 -*-
# Copyright (c) 2014 Plivo Team. See LICENSE.txt for details.
import os
import argparse
import multiprocessing
import ConfigParser

import gunicorn.app.base
from gunicorn.six import iteritems

from sharq_server import setup_server, __version__

def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


class SharQServerApplicationRunner(gunicorn.app.base.BaseApplication):

    """A simple SharQ Gunicorn wrapper which is used to load
    config and run the application.
    """

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(SharQServerApplicationRunner, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def run():
    """Exposes a CLI to configure the SharQ Server and runs the server."""
    # create a arg parser and configure it.
    parser = argparse.ArgumentParser(description='SharQ Server.')
    parser.add_argument('-c', '--config', action='store', required=True,
                        help='Absolute path of the SharQ configuration file.',
                        dest='sharq_config')
    parser.add_argument('-gc', '--gunicorn-config', action='store', required=False,
                        help='Gunicorn configuration file.',
                        dest='gunicorn_config')
    parser.add_argument('--version', action='version', version='SharQ Server %s' % __version__)
    args = parser.parse_args()

    # read the configuration file and set gunicorn options.
    config_parser = ConfigParser.SafeConfigParser()
    # get the full path of the config file.
    sharq_config  = os.path.abspath(args.sharq_config)
    config_parser.read(sharq_config)

    host = config_parser.get('sharq-server', 'host')
    port = config_parser.get('sharq-server', 'port')
    bind = '%s:%s' % (host, port)
    try:
        workers = config_parser.get('sharq-server', 'workers')
    except ConfigParser.NoOptionError:
        workers = number_of_workers()

    try:
        accesslog = config_parser.get('sharq-server', 'accesslog')
    except ConfigParser.NoOptionError:
        accesslog = None

    options = {
        'bind': bind,
        'workers': workers,
        'worker_class': 'gevent'  # required for sharq to function.
    }
    if accesslog:
        options.update({
            'accesslog': accesslog
        })

    if args.gunicorn_config:
        gunicorn_config = os.path.abspath(args.gunicorn_config)
        options.update({
            'config': gunicorn_config
        })

    print """
      ___ _              ___    ___
     / __| |_  __ _ _ _ / _ \  / __| ___ _ ___ _____ _ _
     \__ \ ' \/ _` | '_| (_) | \__ \/ -_) '_\ V / -_) '_|
     |___/_||_\__,_|_|  \__\_\ |___/\___|_|  \_/\___|_|

    Version: %s

    Listening on: %s
    """ % (__version__, bind)
    server = setup_server(sharq_config)
    SharQServerApplicationRunner(server.app, options).run()
