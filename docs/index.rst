Welcome to SHARQ!
=================

SHARQ is a flexible, open source, rate limited queuing system. Based on the `Leaky Bucket Algorithm <http://en.wikipedia.org/wiki/Leaky_bucket#The_Leaky_Bucket_Algorithm_as_a_Queue>`_, `SHARQ <https://github.com/plivo/sharq-server>`_ lets you create queues dynamically and update their rate limits in real time.

SHARQ consists of two components - the core component and the server component. The SHARQ core is built on `Redis <https://redis.io/>`_, using Python and Lua, and the SHARQ Server is built using `Flask <http://flask.pocoo.org/>`_ and `Gevent <http://www.gevent.org/>`_ and talks HTTP.

SHARQ is released under the permissive `MIT License <https://github.com/plivo/sharq-server/blob/master/LICENSE.txt>`_ and is `available on Github <https://github.com/plivo/sharq-server>`_!

To learn more about SHARQ, check out the `getting started section <gettingstarted.html>`_.

.. toctree::
   :maxdepth: 2

   installation
   gettingstarted
   configuration
   apireference
   internals
   faqs
   contributing
   license
