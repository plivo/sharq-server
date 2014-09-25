=============
Configuration
=============

The SHARQ configuration file is minimal and has three sections.

* `Sharq Section <#id1>`_
* `Sharq Server Section <#id2>`_
* `Redis Section <#id3>`_


sharq section
~~~~~~~~~~~~~

This section contains the configurations specific to the SHARQ core.

job\_expire\_interval
^^^^^^^^^^^^^^^^^^^^^

``job_expire_interval`` is the number of milliseconds after which any job
not marked as finished will expire. All expired jobs are scheduled for re-queueing.

job\_requeue\_interval
^^^^^^^^^^^^^^^^^^^^^^

``job_requeue_interval`` is the number of milliseconds to wait between
two clean up processes. A clean up re-queues all the expired jobs back into their
respective queues.

sharq-server section
~~~~~~~~~~~~~~~~~~~~

This section contains the configurations specific to the SHARQ Server.

host
^^^^

``host`` is IP address to which the SHARQ Server should bind to.

port
^^^^

``port`` is where the SHARQ Server should listen for requests.

workers
^^^^^^^

SHARQ Server internally uses `Gunicorn <http://gunicorn.org/>`_ as the server. The ``workers`` parameter specifies the number of Gunicorn workers to spawn when the server starts. More details on this can be found in the `Gunicorn docs <http://docs.gunicorn.org/en/latest/settings.html#workers>`_.

accesslog
^^^^^^^^^

Location for the SHARQ Server to write its access logs.

redis section
~~~~~~~~~~~~~

This section contains the configurations specific to Redis.

db
^^

The Redis database number to which the SHARQ Server should connect.

key\_prefix
^^^^^^^^^^^

Every key used by the SHARQ Server in Redis will start with this prefix.

conn\_type
^^^^^^^^^^

Specifies how the SHARQ Server should connect to Redis. If Redis is in
the same machine as the SHARQ Server, then connecting via unix socket (*unix_sock*)
is recommended.

If Redis is on a remote machine, set ``conn\_type`` to *tcp_sock*.

unix\_socket\_path
^^^^^^^^^^^^^^^^^^

Absolute path of the unix socket created by Redis. This has to be set in
case the ``conn\_type`` is set to *unix_sock*.

port
^^^^

Port where Redis listens for connections.

host
^^^^

IP address or FQDN of Redis.


A Sample Configuration File
~~~~~~~~~~~~~~~~~~~~~~~~~~~

A sample configuration file looks like this. You can also get this configuration file from the `Github repository <https://raw.githubusercontent.com/plivo/sharq-server/master/sharq.conf>`_.

.. code-block:: ini

    [sharq]
    job_expire_interval  : 1000 ; in milliseconds
    job_requeue_interval : 1000 ; in milliseconds

    [sharq-server]
    host                 : 127.0.0.1
    port                 : 8080
    workers              : 1 ; optional
    accesslog            : /tmp/sharq.log ; optional

    [redis]
    db                   : 0
    key_prefix           : sharq_server
    conn_type            : tcp_sock ; or unix_sock
    ;; unix connection settings
    unix_socket_path     : /tmp/redis.sock
    ;; tcp connection settings
    port                 : 6379
    host                 : 127.0.0.1
