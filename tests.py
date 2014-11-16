# -*- coding: utf-8 -*-
# Copyright (c) 2014 Plivo Team. See LICENSE.txt for details.
import unittest
import ujson as json
from sharq_server import setup_server


class SharQServerTestCase(unittest.TestCase):

    def setUp(self):
        # get test client & redis connection
        server = setup_server('./sharq.conf')
        self.app = server.app.test_client()
        self.r = server.sq._r

        # flush redis
        self.r.flushdb()

    def test_root(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.data), {'message': 'Hello, SharQ!'})

    def test_enqueue(self):
        request_params = {
            'job_id': 'ef022088-d2b3-44ad-bf0d-a93d6d93b82c',
            'payload': {'message': 'Hello, world.'},
            'interval': 1000
        }
        response = self.app.post(
            '/enqueue/sms/johdoe/', data=json.dumps(request_params),
            content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'queued')

        request_params = {
            'job_id': 'ef022088-d2b3-44ad-bf1d-a93d6d93b82c',
            'payload': {'message': 'Hello, world.'},
            'interval': 1000,
            'requeue_limit': 10
        }
        response = self.app.post(
            '/enqueue/sms/johdoe/', data=json.dumps(request_params),
            content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'queued')

    def test_dequeue_fail(self):
        response = self.app.get('/dequeue/')
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'failure')

        response = self.app.get('/dequeue/sms/')
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'failure')

    def test_dequeue(self):
        # enqueue a job
        request_params = {
            'job_id': 'ef022088-d2b3-44ad-bf0d-a93d6d93b82c',
            'payload': {'message': 'Hello, world.'},
            'interval': 1000
        }
        self.app.post(
            '/enqueue/sms/johndoe/', data=json.dumps(request_params),
            content_type='application/json')

        # dequeue a job
        response = self.app.get('/dequeue/sms/')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'success')
        self.assertTrue(
            response_data['job_id'], 'ef022088-d2b3-44ad-bf0d-a93d6d93b82c')
        self.assertEqual(
            response_data['payload'], {'message': 'Hello, world.'})
        self.assertEqual(response_data['queue_id'], 'johndoe')
        self.assertEqual(response_data['requeues_remaining'], -1)  # from the config

    def test_finish_fail(self):
        # mark a non existent job as finished
        response = self.app.post(
            '/finish/sms/johndoe/ef022088-d2b3-44ad-bf0d-a93d6d93b82c/')
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'failure')

    def test_finish(self):
        # enqueue a job
        request_params = {
            'job_id': 'ef022088-d2b3-44ad-bf0d-a93d6d93b82c',
            'payload': {'message': 'Hello, world.'},
            'interval': 1000
        }
        self.app.post(
            '/enqueue/sms/johndoe/', data=json.dumps(request_params),
            content_type='application/json')

        # dequeue a job
        self.app.get('/dequeue/sms/')

        # mark the job as finished
        response = self.app.post(
            '/finish/sms/johndoe/ef022088-d2b3-44ad-bf0d-a93d6d93b82c/')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'success')

    def test_interval(self):
        # enqueue a job
        request_params = {
            'job_id': 'ef022088-d2b3-44ad-bf0d-a93d6d93b82c',
            'payload': {'message': 'Hello, world.'},
            'interval': 1000
        }
        self.app.post(
            '/enqueue/sms/johndoe/', data=json.dumps(request_params),
            content_type='application/json')

        # change the interval
        request_params = {
            'interval': 5000
        }
        response = self.app.post(
            '/interval/sms/johndoe/', data=json.dumps(request_params),
            content_type='application/json')
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'success')

    def test_interval_fail(self):
        # change the interval
        request_params = {
            'interval': 5000
        }
        response = self.app.post(
            '/interval/sms/johndoe/', data=json.dumps(request_params),
            content_type='application/json')
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'failure')

    def test_metrics(self):
        response = self.app.get('/metrics/')
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'success')
        self.assertIn('queue_types', response_data)
        self.assertIn('enqueue_counts', response_data)
        self.assertIn('dequeue_counts', response_data)

    def test_metrics_with_queue_type(self):
        response = self.app.get('/metrics/sms/')
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'success')
        self.assertIn('queue_ids', response_data)

    def test_metrics_with_queue_type_and_queue_id(self):
        response = self.app.get('/metrics/sms/johndoe/')
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'success')
        self.assertIn('queue_length', response_data)
        self.assertIn('enqueue_counts', response_data)
        self.assertIn('dequeue_counts', response_data)

    def tearDown(self):
        # flush redis
        self.r.flushdb()

if __name__ == '__main__':
    unittest.main()
