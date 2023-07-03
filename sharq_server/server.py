# -*- coding: utf-8 -*-
# Copyright (c) 2014 Plivo Team. See LICENSE.txt for details.
import os
import gevent
import configparser
import ujson as json
from flask import Flask, request, jsonify
from redis.exceptions import LockError
import traceback
from sharq import SharQ


class SharQServer(object):
    """Defines a HTTP based API on top of SharQ and
    exposed the app to run the server.
    """

    def __init__(self, config_path):
        """Load the SharQ config and define the routes."""
        # read the configs required by sharq-server.
        self.config = configparser.SafeConfigParser()
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
        self.app.add_url_rule(
            '/deletequeue/<queue_type>/<queue_id>/',
            view_func=self._view_clear_queue, methods=['DELETE'])
        self.app.add_url_rule(
            '/deepstatus/',
            view_func=self._view_deep_status, methods=['GET'])

    def requeue(self):
        """Loop endlessly and requeue expired jobs."""
        job_requeue_interval = float(
            self.config.get('sharq', 'job_requeue_interval'))
        while True:
            try:
                self.sq.requeue()
            except Exception as e:
                traceback.print_exc()
            gevent.sleep(job_requeue_interval / 1000.00)  # in seconds

    def requeue_with_lock(self):
        """Loop endlessly and requeue expired jobs, but with a distributed lock"""
        enable_requeue_script = self.config.get('sharq', 'enable_requeue_script')
        if enable_requeue_script == "false":
            print("requeue script disabled")
            return

        job_requeue_interval = float(
            self.config.get('sharq', 'job_requeue_interval'))

        print("start requeue loop: job_requeue_interval = %f" % (job_requeue_interval))
        while True:
            try:
                with self.sq.redis_client().lock('sharq-requeue-lock-key', timeout=15):
                    try:
                        self.sq.requeue()
                    except Exception as e:
                        traceback.print_exc()
            except LockError:
                # the lock wasn't acquired within specified time
                pass
            finally:
                gevent.sleep(job_requeue_interval / 1000.00)  # in seconds

    def _view_index(self):
        """Greetings at the index."""
        return jsonify(**{'message': 'Hello, SharQ!'})

    def _view_enqueue(self, queue_type, queue_id):
        """Enqueues a job into SharQ."""
        print('Inside _view_enqueue function')
        response = {
            'status': 'failure'
        }
        try:
            request_data = json.loads(request.data)
        except Exception as e:
            response['message'] = e.message
            return jsonify(**response), 400

        request_data.update({
            'queue_type': queue_type,
            'queue_id': queue_id
        })

        max_queued_length = request_data['payload'].get('max_queued_length', 7200)

        enqueue_allow = self.sq.get_queue_length(queue_type, queue_id, max_queued_length)
        if enqueue_allow:
            try:
                response = self.sq.enqueue(**request_data)
            except Exception as e:
                traceback.print_exc()
                response['message'] = e.message
                return jsonify(**response), 400

            return jsonify(**response), 201
        else:
            response['message'] = 'Max call queue reached'
            return jsonify(**response), 429

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
        except Exception as e:
            import traceback
            for line in traceback.format_exc().splitlines():
                print(line)
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
        except Exception as e:
            traceback.print_exc()
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
        except Exception as e:
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
        except Exception as e:
            traceback.print_exc()
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
        except Exception as e:
            traceback.print_exc()
            response['message'] = e.message
            return jsonify(**response), 400

        return jsonify(**response)

    def _view_deep_status(self):
        """Checks  underlying data store health"""
        try:

            self.sq.deep_status()
            response = {
                'status': "success"
            }
            return jsonify(**response)
        except Exception as e:
            print(e)
            import traceback
            for line in traceback.format_exc().splitlines():
                print(line)
            raise Exception

    def _view_clear_queue(self, queue_type, queue_id):
        """remove queue from SharQ based on the queue_type and queue_id."""
        response = {
            'status': 'failure'
        }
        try:
            request_data = json.loads(request.data)
        except Exception as e:
            response['message'] = e.message
            return jsonify(**response), 400
        
        request_data.update({
            'queue_type': queue_type,
            'queue_id': queue_id
        })
        try:
            response = self.sq.clear_queue(**request_data)
        except Exception as e:
            traceback.print_exc()
            response['message'] = e.message
            return jsonify(**response), 400

        return jsonify(**response)


def setup_server(config_path):
    """Configure SharQ server, start the requeue loop
    and return the server."""
    # configure the SharQ server
    server = SharQServer(config_path)
    # start the requeue loop
    gevent.spawn(server.requeue_with_lock)

    return server
