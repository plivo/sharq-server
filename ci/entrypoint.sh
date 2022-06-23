#!/usr/bin/env bash

set -e


CONSUL=$CONSUL


echo "
      ___ _              ___    ___
     / __| |_  __ _ _ _ / _ \  / __| ___ _ ___ _____ _ _
     \__ \ ' \/ _' | '_| (_) | \__ \/ -_) '_\ V / -_) '_|
     |___/_||_\__,_|_|  \__\_\ |___/\___|_|  \_/\___|_|

     "

/usr/sbin/consul-template \
    -consul-addr "$CONSUL" \
    -template "/app/config/sharq.conf.ctmpl:/app/config/sharq.conf" \
    -consul-retry-attempts=0 -once

echo "All templates are rendered. Starting sharq-server..."

# Start Supervisor, with Nginx and sharq-server
exec /usr/bin/supervisord -n -c /etc/supervisord.conf
