# -*- coding: utf-8 -*-
# Copyright (c) 2014 Plivo Team. See LICENSE.txt for details.
import os
import gevent
import ConfigParser
import ujson as json
from flask import Flask, request, jsonify

from sharq import SharQ


class SharQServer(object):
    """Defines a HTTP based API on top of SharQ and
    exposed the app to run the server.
    """

    def __init__(self, config_path):
        """Load the SharQ config and define the routes."""
        # read the configs required by sharq-server.
        self.config = ConfigParser.SafeConfigParser()
        self.config.read(config_path)
        # pass the config file to configure the SharQ core.
        self.sq = SharQ(config_path)

        self.app = Flask(__name__)
        # set the routes
        self.app.add_url_rule(
            '/', view_func=self._view_index, methods=['GET'])
        self.app.add_url_rule(
            '/enqueue/<queue_type>/<queue_id>/',
            view_func=self._view_enqueue, methods=['POST'])
        self.app.add_url_rule(
            '/dequeue/', defaults={'queue_type': 'default'},
            view_func=self._view_dequeue, methods=['GET'])
        self.app.add_url_rule(
            '/dequeue/<queue_type>/',
            view_func=self._view_dequeue, methods=['GET'])
        self.app.add_url_rule(
            '/finish/<queue_type>/<queue_id>/<job_id>/',
            view_func=self._view_finish, methods=['POST'])
        self.app.add_url_rule(
            '/interval/<queue_type>/<queue_id>/',
            view_func=self._view_interval, methods=['POST'])
        self.app.add_url_rule(
            '/metrics/', defaults={'queue_type': None, 'queue_id': None},
            view_func=self._view_metrics, methods=['GET'])
        self.app.add_url_rule(
            '/metrics/<queue_type>/', defaults={'queue_id': None},
            view_func=self._view_metrics, methods=['GET'])
        self.app.add_url_rule(
            '/metrics/<queue_type>/<queue_id>/',
            view_func=self._view_metrics, methods=['GET'])

    def requeue(self):
        """Loop endlessly and requeue expired jobs."""
        job_requeue_interval = float(
            self.config.get('sharq', 'job_requeue_interval'))
        while True:
            self.sq.requeue()
            gevent.sleep(job_requeue_interval / 1000.00)  # in seconds

    def _view_index(self):
        """Greetings at the index."""
        return jsonify(**{'message': 'Hello, SharQ!'})

    def _view_enqueue(self, queue_type, queue_id):
        """Enqueues a job into SharQ."""
        response = {
            'status': 'failure'
        }
        try:
            request_data = json.loads(request.data)
        except Exception, e:
            response['message'] = e.message
            return jsonify(**response), 400

        request_data.update({
            'queue_type': queue_type,
            'queue_id': queue_id
        })

        try:
            response = self.sq.enqueue(**request_data)
        except Exception, e:
            response['message'] = e.message
            return jsonify(**response), 400

        return jsonify(**response), 201

    def _view_dequeue(self, queue_type):
        """Dequeues a job from SharQ."""
        response = {
            'status': 'failure'
        }

        request_data = {
            'queue_type': queue_type
        }
        try:
            response = self.sq.dequeue(**request_data)
            if response['status'] == 'failure':
                return jsonify(**response), 404
        except Exception, e:
            response['message'] = e.message
            return jsonify(**response), 400

        return jsonify(**response)

    def _view_finish(self, queue_type, queue_id, job_id):
        """Marks a job as finished in SharQ."""
        response = {
            'status': 'failure'
        }
        request_data = {
            'queue_type': queue_type,
            'queue_id': queue_id,
            'job_id': job_id
        }

        try:
            response = self.sq.finish(**request_data)
            if response['status'] == 'failure':
                return jsonify(**response), 404
        except Exception, e:
            response['message'] = e.message
            return jsonify(**response), 400

        return jsonify(**response)

    def _view_interval(self, queue_type, queue_id):
        """Updates the queue interval in SharQ."""
        response = {
            'status': 'failure'
        }
        try:
            request_data = json.loads(request.data)
            interval = request_data['interval']
        except Exception, e:
            response['message'] = e.message
            return jsonify(**response), 400

        request_data = {
            'queue_type': queue_type,
            'queue_id': queue_id,
            'interval': interval
        }

        try:
            response = self.sq.interval(**request_data)
            if response['status'] == 'failure':
                return jsonify(**response), 404
        except Exception, e:
            response['message'] = e.message
            return jsonify(**response), 400

        return jsonify(**response)

    def _view_metrics(self, queue_type, queue_id):
        """Gets SharQ metrics based on the params."""
        response = {
            'status': 'failure'
        }
        request_data = {}
        if queue_type:
            request_data['queue_type'] = queue_type
        if queue_id:
            request_data['queue_id'] = queue_id

        try:
            response = self.sq.metrics(**request_data)
        except Exception, e:
            response['message'] = e.message
            return jsonify(**response), 400

        return jsonify(**response)


def setup_server(config_path):
    """Configure SharQ server, start the requeue loop
    and return the server."""
    # configure the SharQ server
    server = SharQServer(config_path)
    # start the requeue loop
    gevent.spawn(server.requeue)

    return server
