[uwsgi]
# automatically start master process
master = true

# try to autoload appropriate plugin if "unknown" option has been specified
autoload = true

# spawn n uWSGI worker processes
workers = {{ UWSGI_WORKER }}

# automatically kill workers on master's death
no-orphans = true

# write master's pid in file /run/uwsgi/<confnamespace>/<confname>/pid
pidfile = /var/run/sharq/uwsgi.pid

# bind to UNIX socket at /run/uwsgi/<confnamespace>/<confname>/socket
socket = /var/run/sharq/sharq.sock

# set mode of created UNIX socket
chmod-socket = 666

# disable logging
disable-logging=True

# daemonize
daemonize = true

# sharq related
chdir = /opt/sharq-server
virtualenv = /opt/sharq-server
module = wsgi:app
gevent = 1024

# configure sharq config path
env = SHARQ_CONFIG=/etc/sharq-server/config/sharq.conf