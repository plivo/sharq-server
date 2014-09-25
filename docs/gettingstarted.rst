===============
Getting Started
===============

Once the SHARQ Server is installed, it will expose a **sharq-server** command. If you have not yet installed the SHARQ Server, refer `here <installation.html>`_ for instructions.

The **sharq-server** command is minimal and accepts a SHARQ configuration file. To get started quickly, fetch the `SHARQ sample configuration file <https://raw.githubusercontent.com/plivo/sharq-server/master/sharq.conf>`_. Refer to the `configuration section <configuration.html>`_ for more details.

Running the SHARQ Server
------------------------

The SHARQ Server can be started with the following command.

::

    sharq-server --config sharq.conf


This will run the SHARQ Server in the foreground with the following output.

::

      ___ _              ___    ___
     / __| |_  __ _ _ _ / _ \  / __| ___ _ ___ _____ _ _
     \__ \ ' \/ _` | '_| (_) | \__ \/ -_) '_\ V / -_) '_|
     |___/_||_\__,_|_|  \__\_\ |___/\___|_|  \_/\___|_|

    Version: 0.1.0

    Listening on: 127.0.0.1:8080


Ensure the SHARQ Server has started up correctly by making an HTTP GET request to the server root.


.. code-block:: bash

    curl http://127.0.0.1:8080/
    {
      "message": "Hello, SharQ!"
    }


SHARQ Workflow
--------------

Before using SHARQ, understand its workflow as summarized in the following points:

* **Enqueue** a job into the queue with parameters like ``queue_type``, ``queue_id``, ``interval``, etc. The interval parameter specifies the rate limit of the queue into which the job is being enqueued.
* **Dequeue** a job from the queue by specifying the ``queue_type``. The dequeue is non-blocking. This means that dequeue succeeds only if there is any job ready to be dequeued (based on the rate limit) from any of the queues of the type specified by ``queue_type``.
* Once the job has be dequeued, it is the responsibility of the worker to mark the job as successfully complete by making a **Finish** request. If the SHARQ Server does not receive a finish request within a preset interval, it re-queues the job back into the queue. This enables the SHARQ Server to make this job available to the workers, on future dequeue requests.

Now that you have understood the basic workflow of SHARQ Server, go ahead and try out the SHARQ API as shown below.


SHARQ API Examples
------------------

Enqueue
```````

The enqueue API will push the job into the SHARQ Server. Enqueue comes with a lot of parameters which makes SHARQ flexible. A typical enqueue request looks like this:

.. code-block:: bash

    curl -H "Accept: application/json" \
    -H "Content-type: application/json" \
    -X POST -d ' {"job_id": "b81c07a7-5bba-4790-ab40-a061994088c1", "interval": 1000, "payload": {"message": "hello, world"}}' \
    http://localhost:8080/enqueue/sms/1/


Here is a break down of the above request. To translate the `cURL <http://curl.haxx.se/>`_ request in normal English, an HTTP POST request is made to the url ``http://localhost:8080/enqueue/sms/1/`` with a JSON payload in the request body. The JSON payload is as follows:

.. code-block:: python

    {
      "job_id": "b81c07a7-5bba-4790-ab40-a061994088c1",
      "interval": 1000,
      "payload": {"message": "hello, world"}
    }

The url is of the form: ``http://hostname:port/enqueue/<queue_type>/<queue_id>/``.

Each queue is uniquely identified by the ``queue_type`` and ``queue_id`` pair. Any job sent to this url will be pushed into this specific queue. Each job pushed into this queue is identified by the ``job_id``. The ``queue_type`` and ``queue_id`` pair has to be universally unique but the ``job_id`` can be unique at a queue level.

The ``interval`` parameter is of pivotal importance in SHARQ. It is this parameter which defines the rate limit of the queue. Each queue identified by the ``queue_type``, ``queue_id`` pair can be set a rate limit (the inverse of interval). For example, if the queue has to be rate limited at 1 request per second, the ``interval`` has to be set to 1000 (in milliseconds).

The ``payload`` is a JSON formatted blob which is the actual content that is being queued. This can be any message which has to be transmitted in the queue.

When the enqueue request succeeds, the SHARQ Server responds with an HTTP status 201 and a message saying:

.. code-block:: python

    {
      "status": "queued"
    }


A simple Python snippet to illustrate this using the `Requests Python module <http://docs.python-requests.org/en/latest/>`_ can be found `here <https://gist.github.com/sandeepraju/bfa72c7027e1d739b33e>`_.

Dequeue
```````

The dequeue API will pull the job from the SHARQ Server. The dequeue request will look for jobs in a particular ``queue_type``. Depending on whether any queue (with ``queue_id``) of that ``queue_type`` is ready to be dequeued (based on the rate limit set while enqueuing), the SHARQ Server returns a job or returns a dequeue failure.

A simple successful dequeue request looks like this:

.. code-block:: bash

    curl http://localhost:8080/dequeue/sms/

Here, *sms* is the ``queue_type``. The above request is trying to dequeue a job from any of the queues of type *sms*. If the job is ready, the SHARQ Server responds with an HTTP status 200 and the following content:

.. code-block:: python

    {
      "job_id": "b81c07a7-5bba-4790-ab40-a061994088c1",
      "payload": {
	"message": "hello, world"
      },
      "queue_id": "1",
      "status": "success"
    }

**NOTE:**

* It is important to note that dequeue does not actually remove the job from the SHARQ Server. Internally, SHARQ changes the state of this job from *pending* to *active* when a dequeue happens. Every dequeue has to be accompanied with a finish request to mark the job as successfully completed. This notifies the SHARQ Server to remove the job completely. If a finish request is not received by SHARQ within a specific time after a successful dequeue, SHARQ assumes the job as failed (marks it as *expired*) and re-queues it back into the queue. This time interval for which the SHARQ Server waits before marking the job as *expired* is called the ``job_expire_interval``. This parameter can be set in the configuration file.
* As the dequeue request is non-blocking, it is a common pattern to make the dequeue request in a loop. The SHARQ Server returns a HTTP status 200 on success and a 404 on failure.

A simple Python snippet to illustrate a simple SHARQ worker using the `Requests Python module <http://docs.python-requests.org/en/latest/>`_ can be found `here <https://gist.github.com/sandeepraju/d733e87e1a735d382d6a>`_.


Finish
``````

The finish API will mark any dequeued job as successfully completed. This notifies the SHARQ Server to remove the job from its system as the job has been acknowledged by the worker as successfully completed.

A finish request will look like this:

.. code-block:: bash

    curl -X POST http://localhost:8080/finish/sms/1/b81c07a7-5bba-4790-ab40-a061994088c1/

The above request example makes a finish request to the SHARQ Server with ``job_id`` *b81c07a7-5bba-4790-ab40-a061994088c1* belonging to the ``queue_id`` *1* and of ``queue_type`` *sms*. So, the finish request is of the form ``http://hostname:port/finish/<queue_type>/<queue_id>/<job_id>/``.

The SHARQ Server responds with a status code of 200 and the following message when the finish request succeeds:

.. code-block:: python

    {
      "status": "success"
    }


A simple Python snippet to illustrate a minimal but complete SHARQ worker with finish using the `Requests Python module <http://docs.python-requests.org/en/latest/>`_ can be found `here <https://gist.github.com/sandeepraju/3da0ad035aa9bf5504b1>`_.

The SHARQ Server waits for the finish request after a dequeue for a specified time interval before marking the job as *expired* and further re-queueing the job back into the queue. Any job which gets a finish request within this interval will be marked as *successful* and removed from the SHARQ Server. This wait interval can be set in the configuration file. The ``job_expire_interval`` in the configuration file, specifies the time interval which the SHARQ Server waits for a dequeue request, from the worker, before marking a job as *expired* (ready to be re-queued back). The ``job_requeue_interval`` in the configuration file, specifies the time interval between two clean up operations on the SHARQ Server. A clean up operation is the process of re-queuing all jobs that are marked as *expired*.

The SHARQ Server contains an `Internal API <apireference.html#interval>`_ to update the rates of queues in real time. It also contains a `Metrics API <apireference.html#metrics>`_ to get basic information such as the queue length, list of active queues, and so on. Check out the `API Reference <apireference.html>`_ section for more details.
