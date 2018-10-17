#!/usr/bin/env bash

set -e


CONSUL=$CONSUL


echo "[ENTRYPOINT] - Starting SharQServer."

/usr/sbin/consul-template \
    -consul-addr "$CONSUL" \
    -template "/etc/sharq-server/config/sharq.conf.ctmpl:/etc/sharq-server/config/sharq.conf" \
    -template "/etc/sharq-server/config/sharq.ini.ctmpl:/etc/sharq-server/config/sharq.ini"
    -consul-retry-attempts=0 \
    -exec "/opt/sharq-server/bin/uwsgi --ini /etc/sharq-server/config/sharq.ini && nginx -g 'daemon off;'"
