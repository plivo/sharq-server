===========================
Frequently Asked  Questions
===========================

When should I use SHARQ?
========================

If you want the flexibility to dynamically create queues and update their rate limits in real time without making any configuration changes, then you need SHARQ.

How do I set a rate limit for a queue?
======================================

The rate limit of a queue (which is the inverse of an interval), can be set while making an enqueue request. Each enqueue request requires the ``interval`` parameter which defines the rate limit of the queue. For example, if the queue has to be rate limited at 1 request per second, the ``interval`` has to be set to 1000 (in milliseconds). Refer to the `Getting Started <gettingstarted.html>`_ section to know more about how to set the interval while making an enqueue request.

How do I change the rate limit of a queue?
==========================================

Once the rate limit has been set for a queue during the enqueue operation, it can be changed using the `Interval API <apireference.html#interval>`_.

How do I write a SHARQ worker for processing jobs from the SHARQ Server?
========================================================================

A simple SHARQ worker polls for the jobs in a loop. The `Python snippet <https://gist.github.com/sandeepraju/3da0ad035aa9bf5504b1>`_ below shows how to structure a minimal worker:

.. code-block:: python

    import time
    import json
    import requests

    while True:
	# dequeue the job from the queue of type `sms`
	try:
	    response = requests.get('http://localhost:8080/dequeue/sms/')
	    if response.status_code == 200:
		# successful dequeue.
		r = json.loads(response.text)
		print r['payload']  # process the payload here.
		queue_id = r['queue_id']
		job_id = r['job_id']
		# mark the job as completed successfully by
		# sending a finish request.
		requests.post(
		    'http://localhost:8080/finish/sms/%s/%s/' % (
		    queue_id, job_id))
	    elif response.status_code == 404:
		# no job found (either queue is empty or none
		# of the jobs are ready yet).
		time.sleep(1)  # wait for a second before retrying if needed.
	except Exception as e:
	    print "Something went wrong!"
	    time.sleep(5)  # retry after 5 seconds.


How do I configure the time of expiry of a job?
===============================================

Any job which is dequeued by the worker has to be acknowledged with a finish request within a specific time period, to mark that job as successfully processed. The job which does not get a finish request within this period will be marked as *expired* by the SHARQ Server. This time period has to be specified by the ``job_expire_interval`` parameter in the SHARQ configuration file.


How do I configure when the expired jobs should be re-queued?
=============================================================

All expired jobs in the SHARQ Server will be re-queued back into their respective queues during the *clean up* process. The time interval between two clean ups can be specified by the ``job_requeue_interval`` parameter in the SHARQ configuration file.

Is there a way to run the SHARQ Server using uWSGI?
===================================================

Yes! By default the SHARQ Server uses `Gunicorn <http://gunicorn.org/>`_ internally. If you want to use `uWSGI <https://uwsgi-docs.readthedocs.org/en/latest/>`_ or any other server based on WSGI, you can do so by running ``wsgi.py`` provided in the source files `available on Github <https://github.com/plivo/sharq-server/blob/master/wsgi.py>`_. For optimal performance, it is recommended to use  uWSGI with `Nginx <http://nginx.org/>`_. More details can be found in the `uWSGI documentation <http://uwsgi-docs.readthedocs.org/en/latest/Nginx.html>`_.

How do I know the number of jobs in any queue in real time?
===========================================================

The `Metrics API <apireference.html#metrics>`_ lets you query the SHARQ Server for details like number of jobs, per minute enqueue & dequeue rates, and so on. Read the `API Reference <apireference.html#metrics>`_ section for more details.

How do I get a list of all queues in the SHARQ Server?
======================================================

The `Metrics API <apireference.html#metrics>`_ lets you query the SHARQ Server for details like number of jobs, per minute enqueue & dequeue rates, and so on. Read the `API Reference <apireference.html#metrics>`_ section for more details.

How do I check the status of a job in real time?
================================================

This feature is not yet available in SHARQ but will be implemented in the future.

Where can I find the source code of SHARQ?
==========================================

The SHARQ code base is split into two components - the core component and the server component. You can find it here:

**Github Repository Links:**

* The SHARQ Core - https://github.com/plivo/sharq
* The SHARQ Server - https://github.com/plivo/sharq-server

Read the `Contributing <contributing.html>`_ section for more details.

I just found a bug. How do I report it?
=======================================

Read the `Contributing <contributing.html>`_ section for more details.
