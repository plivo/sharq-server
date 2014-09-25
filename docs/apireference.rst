=============
API Reference
=============

This section contains a very brief introduction to the SHARQ API. If you are looking to get started with SHARQ, refer to the `getting started section <gettingstarted.html>`_ before reading this.

Enqueue
~~~~~~~

Enqueue a job into the SHARQ Server.

::

    POST /enqueue/<queue_type>/<queue_id>/

**Request (Raw JSON POST data):**

::

    {
      "job_id": "b81c07a7-5bba-4790-ab40-a061994088c1",
      "interval": 1000,
      "payload": {"hello": "world"}
    }

**Response (success):**

Status Code: 201

::

    {
      "status": "queued"
    }

**Response (bad request):**

Status Code: 400

::

    {
        "message": "`queue_type` is a mandatory parameter",
        "status": "failure"
    }

**cURL Example:**

::

    $curl -H "Accept: application/json" \
    -H "Content-type: application/json" \
    -X POST -d ' {"job_id": "b81c07a7-5bba-4790-ab40-a061994088c1", "interval": 1000, "payload": {"hello": "world"}}' \
    http://localhost:8080/enqueue/sms/1/


Dequeue
~~~~~~~

Dequeue a job from the SHARQ Server.

::

    GET /dequeue/<queue_type>/

**Response (success):**

Status Code: 200

::

    {
      "job_id": "b81c07a7-5bba-4790-ab40-a061994088c1",
      "payload": {
        "hello": "world"
      },
      "queue_id": "1",
      "status": "success"
    }

**Response (queue has no job ready):**

Status Code: 404

::

    {
        "status": "failure"
    }

**Response (bad request):** Status Code: 400

::

    {
        "message": "`queue_type` has an invalid value.",
        "status": "failure"
    }

**cURL Example:**

::

    curl http://localhost:8080/dequeue/sms/

Finish
~~~~~~

Mark a dequeued job as finished.

::

    POST /finish/<queue_type>/<queue_id>/<job_id>/

**Response (success):**

Status Code: 200

::

    {
      "status": "success"
    }

**Response (job was not found):**

Status Code: 404

::

    {
      "status": "failure"
    }

**Response (bad request):**

Status Code: 400

::

    {
        "message": "`queue_id` is a mandatory parameter",
        "status": "failure"
    }

**cURL Example:**

::

    curl -X POST http://localhost:8080/finish/sms/1/b81c07a7-5bba-4790-ab40-a061994088c1/

Interval
~~~~~~~~

Updates the interval (and effectively the rate) of any queue. The interval has to be specified in the request body, in the JSON format as shown below:

::

    POST /interval/<queue_type>/<queue_id>/

**Request (Raw JSON POST data):**

::

    {
      "interval": 1000
    }

**Response (success):**

Status Code: 200

::

    {
      "status": "success"
    }

**Response (queue was not found):**

Status Code: 404

::

    {
      "status": "failure"
    }

**Response (bad request):**

Status Code: 400

::

    {
      "message": "`interval` has an invalid value.",
      "status": "failure"
    }

**cURL Example:**

::

    curl -H "Accept: application/json" \
    -H "Content-type: application/json" \
    -X POST -d ' {"interval": 5000}' \
    http://localhost:8080/interval/sms/1/


Metrics
~~~~~~~

The Metrics API enables getting basic metrics from the SHARQ Server.

Global Metrics
^^^^^^^^^^^^^^

Fetches metrics on a global level (the consolidated metrics of all queues in SHARQ) from the SHARQ Server. The response to the API request, contains the enqueue and dequeue counts which show the number of enqueues and dequeues in each minute over a period of 10 minutes.

::

    GET /metrics/

**Response (success):**

Status Code: 200

::

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

**cURL Example:**

::

    curl  http://localhost:8080/metrics/

List Queue Ids
^^^^^^^^^^^^^^

Lists all the queues of a particular queue type in the SHARQ Server.

::

    GET /metrics/<queue_type>/

**Response (success):**

Status Code: 200

::

    {
      "queue_ids": [
        "1"
      ],
      "status": "success"
    }

**cURL Example:**

::

    curl  http://localhost:8080/metrics/sms/

Queue Specific Metrics
^^^^^^^^^^^^^^^^^^^^^^

Fetches metrics specific to a particular queue of a specific queue type. The response to the API request contains the enqueue and dequeue counts for each minute over a 10 minute period. The response also contains the length of the queue at that particular point in time.

::

    GET /metrics/<queue_type>/<queue_id>/

**Response (success):**

Status Code: 200

::

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

**Response (bad request):**

Status Code: 400

::

    {
        "message": "`queue_id` should be accompanied by `queue_type`.",
        "status": "failure"
    }

**cURL Example:**

::

    curl  http://localhost:8080/metrics/sms/1/
