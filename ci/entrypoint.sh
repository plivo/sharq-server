#!/usr/bin/env bash

set -ex


CONSUL=$CONSUL


echo "
      ___ _              ___    ___
     / __| |_  __ _ _ _ / _ \  / __| ___ _ ___ _____ _ _
     \__ \ ' \/ _' | '_| (_) | \__ \/ -_) '_\ V / -_) '_|
     |___/_||_\__,_|_|  \__\_\ |___/\___|_|  \_/\___|_|

     "

/usr/sbin/consul-template \
    -consul-addr "$CONSUL" \
    -template "/etc/sharq-server/config/sharq.conf.ctmpl:/etc/sharq-server/config/sharq.conf" \
    -template "/etc/sharq-server/config/sharq.ini.ctmpl:/etc/sharq-server/config/sharq.ini" \
    -consul-retry-attempts=0 -once \
    -log-level debug

echo "All templates are rendered. Starting sharq-server..."

supervisord -c /etc/supervisord.conf
