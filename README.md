SharQ Server
============

SharQ Server is an rate limited API queuing server based on the [SharQ library](https://github.com/plivo/sharq) and [Redis](https://redis.io).

## Installation

```
pip install sharq-server
```

## Running the server

SharQ server exposes the __sharq-server__ command.

```
usage: sharq-server [-h] -c SHARQ_CONFIG [-gc GUNICORN_CONFIG] [--version]

SharQ Server!

optional arguments:
  -h, --help            show this help message and exit
  -c SHARQ_CONFIG, --config SHARQ_CONFIG
                        Absolute path of the SharQ configuration file.
  -gc GUNICORN_CONFIG, --gunicorn-config GUNICORN_CONFIG
                        Gunicorn configuration file.
  --version             show program's version number and exit
```

SharQ server can be started with the following command. A simple SharQ config file can be [found here](https://github.com/plivo/sharq-server/blob/master/sharq.conf).

```
$sharq-server --config sharq.conf
```

Ensure the SharQ server is up by making a HTTP request.

```
$curl http://127.0.0.1:8080/
{
  "message": "Hello, SharQ!"
}
```

## Getting Started with the SharQ API

### Enqueue

```
POST /enqueue/<queue_type>/<queue_id>/
```
__Request (Raw JSON POST data):__
```
{
  "job_id": "b81c07a7-5bba-4790-ab40-a061994088c1",
  "interval": 1000,
  "payload": {"hello": "world"}
}
```

__Response (success):__

Status Code: 201
```
{
  "status": "queued"
}
```
__Response (bad request):__

Status Code: 400
```
{
    "message": "`queue_type` is a mandatory parameter",
    "status": "failure"
}
```

__cURL Example:__

```
$curl -H "Accept: application/json" \
-H "Content-type: application/json" \
-X POST -d ' {"job_id": "b81c07a7-5bba-4790-ab40-a061994088c1", "interval": 1000, "payload": {"hello": "world"}}' \
http://localhost:8080/enqueue/sms/1/

```

### Dequeue

```
GET /dequeue/<queue_type>/
```

__Response (success):__

Status Code: 200
```
{
  "job_id": "b81c07a7-5bba-4790-ab40-a061994088c1",
  "payload": {
    "hello": "world"
  },
  "queue_id": "1",
  "status": "success"
}
```
__Response (queue has no job ready):__

Status Code: 404
```
{
    "status": "failure"
}
```

__Response (bad request):__
Status Code: 400
```
{
    "message": "`queue_type` has an invalid value.",
    "status": "failure"
}
```
__cURL Example:__
```
curl http://localhost:8080/dequeue/sms/
```

### Finish

```
POST /finish/<queue_type>/<queue_id>/<job_id>/
```

__Response (success):__

Status Code: 200
```
{
  "status": "success"
}
```

__Response (job was not found):__

Status Code: 404
```
{
  "status": "failure"
}
```

__Response (bad request):__

Status Code: 400
```
{
    "message": "`queue_id` is a mandatory parameter",
    "status": "failure"
}
```

__cURL Example:__
```
curl -X POST http://localhost:8080/finish/sms/1/b81c07a7-5bba-4790-ab40-a061994088c1/
```

### Interval

```
POST /interval/<queue_type>/<queue_id>/
```

__Request (Raw JSON POST data):__
```
{
  "interval": 1000
}
```

__Response (success):__

Status Code: 200
```
{
  "status": "success"
}
```

__Response (queue was not found):__

Status Code: 404
```
{
  "status": "failure"
}
```

__Response (bad request):__

Status Code: 400
```
{
  "message": "`interval` has an invalid value.",
  "status": "failure"
}
```

__cURL Example:__
```
curl -H "Accept: application/json" \
-H "Content-type: application/json" \
-X POST -d ' {"interval": 5000}' \
http://localhost:8080/interval/sms/1/
```

### Metrics

#### Global Metrics
```
GET /metrics/
```

__Response (success):__

Status Code: 200
```
{
  "dequeue_counts": {
    "1406200290000": 0,
    "1406200344000": 0,
    "1406200392000": 0,
    "1406200434000": 0,
    "1406200470000": 0,
    "1406200500000": 0,
    "1406200524000": 0,
    "1406200542000": 0,
    "1406200554000": 0,
    "1406200560000": 0
  },
  "enqueue_counts": {
    "1406200290000": 0,
    "1406200344000": 0,
    "1406200392000": 0,
    "1406200434000": 0,
    "1406200470000": 0,
    "1406200500000": 0,
    "1406200524000": 0,
    "1406200542000": 0,
    "1406200554000": 0,
    "1406200560000": 0
  },
  "queue_types": [
    "sms"
  ],
  "status": "success"
}
```

__cURL Example:__
```
curl  http://localhost:8080/metrics/
```
#### List Queue Ids

```
GET /metrics/<queue_type>/
```
__Response (success):__

Status Code: 200
```
{
  "queue_ids": [
    "1"
  ],
  "status": "success"
}
```

__cURL Example:__
```
curl  http://localhost:8080/metrics/sms/
```

#### Queue Specific Metrics

```
GET /metrics/<queue_type>/<queue_id>/
```

__Response (success):__

Status Code: 200
```
{
  "dequeue_counts": {
    "1406200590000": 0,
    "1406200644000": 0,
    "1406200692000": 0,
    "1406200734000": 0,
    "1406200770000": 0,
    "1406200800000": 0,
    "1406200824000": 0,
    "1406200842000": 0,
    "1406200854000": 0,
    "1406200860000": 0
  },
  "enqueue_counts": {
    "1406200590000": 0,
    "1406200644000": 0,
    "1406200692000": 0,
    "1406200734000": 0,
    "1406200770000": 0,
    "1406200800000": 0,
    "1406200824000": 0,
    "1406200842000": 0,
    "1406200854000": 0,
    "1406200860000": 0
  },
  "queue_length": 3,
  "status": "success"
}
```
__Response (bad request):__

Status Code: 400
```
{
    "message": "`queue_id` should be accompanied by `queue_type`.",
    "status": "failure"
}
```

__cURL Example:__
```
curl  http://localhost:8080/metrics/sms/1/
```

## Configuration

### sharq section

#### job_expire_interval

`job_expire_interval` is the number of milliseconds upon which any job not marked as __finished__ will expire.

#### job_requeue_interval

`job_requeue_interval` is the number of milliseconds to wait between two cleanups. A clean up re-queues all the expired jobs into their respective queues.

### sharq-server section

#### host

`host` is the ip address of the SharQ Server.

#### port

`port` where the SharQ server should listen to for requests.

#### workers

The number of `workers` of the SharQ server. Number of workers is the number of parallel requests SharQ server will be able to process.

#### accesslog

The absolute path to where the SharQ access logs are to be written.

### redis section

#### db

The Redis database number to which SharQ should connect.

#### key_prefix

Every key used by SharQ in Redis will start with this prefix.

#### conn_type

Specifies how SharQ should connect to Redis. If the Redis server is in the same machine as the SharQ Server, then connection via `unix_sock` is recommended.

If the Redis is on a remote machine, set _conn_type_ to `tcp_sock`.

#### unix_socket_path

Absolute path of the unix socket created by Redis. This has to be set in case the _conn_type_ is set to `unix_sock`.

#### port

port where Redis server listens for connections.

#### host

IP address or FQDN of the Redis Server

#### A Sample Configuration File
```
[sharq]
job_expire_interval  : 1000 ; in milliseconds
job_requeue_interval : 1000 ; in milliseconds

[sharq-server]
host                 : 127.0.0.1
port                 : 8080
workers              : 1 ; optional
accesslog            : /var/log/sharq-server/sharq.log ; optional

[redis]
db                   : 0
key_prefix           : sharq_server
conn_type            : unix_sock ; or tcp_sock
;; unix connection settings
unix_socket_path     : /tmp/redis.sock
;; tcp connection settings
port                 : 6379
host                 : 127.0.0.1
```

## License

```
The MIT License (MIT)

Copyright (c) 2014 Plivo Inc

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
