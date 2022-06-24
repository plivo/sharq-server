#! /usr/bin/env sh
set -e

# Start Supervisor, with Nginx and sharq-server
exec /usr/bin/supervisord -n -c /etc/supervisord.conf