#!/usr/bin/env bash

set -e


CONSUL=$CONSUL


echo "[ENTRYPOINT] - Starting SharQServer."

/usr/sbin/consul-template \
    -consul-addr "$CONSUL" \
    -template "/etc/sharq-server/config/sharq.conf.ctmpl:/etc/sharq-server/config/sharq.conf" \
    -template "/etc/sharq-server/config/sharq.ini.ctmpl:/etc/sharq-server/config/sharq.ini" \
    -exec "supervisord -c /etc/supervisord.conf"
