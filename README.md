SHARQ Server
============

SHARQ Server is an flexible, rate limited queuing system based on the [SHARQ Core library](https://github.com/plivo/sharq) and [Redis](https://redis.io).

## Overview

SHARQ Server is a flexible, open source, rate limited queuing system. Based on the [Leaky Bucket Algorithm](http://en.wikipedia.org/wiki/Leaky_bucket#The_Leaky_Bucket_Algorithm_as_a_Queue), SHARQ lets you create queues dynamically and update their rate limits in real time.

SHARQ consists of two components - the core component and the server component. The [SHARQ core](https://github.com/plivo/sharq) is built on [Redis](https://redis.io), using Python and Lua, and the SHARQ Server is built using [Flask](http://flask.pocoo.org/) and [Gevent](http://www.gevent.org/) and talks HTTP.

## Installation

SHARQ Server can be installed using [pip](http://pip.readthedocs.org/en/latest/installing.html) as follows:

```
pip install sharqserver
```

## Running the server

SHARQ server can be started with the following command. A simple SHARQ config file can be [found here](https://github.com/plivo/sharq-server/blob/master/sharq.conf).

```
$sharq-server --config sharq.conf
```

Ensure the SHARQ server is up by making a HTTP request.

```
$curl http://127.0.0.1:8080/
{
  "message": "Hello, SharQ!"
}
```

## Documentation

Check out [sharq.io](http://sharq.io) for documentation.

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
