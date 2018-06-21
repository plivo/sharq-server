[sharq]
job_expire_interval  : 5000 ; in milliseconds
job_requeue_interval : 1000 ; in milliseconds
default_job_requeue_limit : -1 ; retries infinitely

[sharq-server]
host                 : 127.0.0.1
port                 : 8080
;; workers              : 32 ; optional commenting out to ensure sharq worker is dependent on number of CPUs
accesslog            : /tmp/sharq.log ; optional

[redis]
db                   : 0
key_prefix           : sharq_server
conn_type            : tcp_sock ; or tcp_sock
;; unix connection settings
;; unix_socket_path     : /var/run/redis/redis.sock
;; tcp connection settings
port                 : 6379
host                 : {{ SHARQ_REDIS }}