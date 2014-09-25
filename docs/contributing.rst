============
Contributing
============

SHARQ is open source and released under the permissive `MIT License <opensource.org/licenses/MIT>`_. No software is complete and bugfree. If you feel something can be improved in SHARQ or would like to report bugs, feel free to do so. Pull requests are always welcome!

SHARQ consists of two components architecturally and with respect to codebases.

1. The `SHARQ Core <https://github.com/plivo/sharq>`_ which implements the core functionality of SHARQ which is rate limiting.
2. The `SHARQ Server <https://github.com/plivo/sharq-server>`_ which exposes an HTTP interface via `Flask <http://flask.pocoo.org/>`_ & `Gevent <http://www.gevent.org/>`_.

The core rate limiting algorithm is implemented in Lua. The detailed explanation of the algorithm with the implementation details and the `Redis <https://redis.io/>`_ data structures can be found in `The Internals </internals.html>`_ section.


**Github Repository Links:**

* https://github.com/plivo/sharq-server
* https://github.com/plivo/sharq
