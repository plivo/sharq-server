from redis_helper import RedisConnection
MAX_ALLOWED_HOURS = 6


def validate_queue_length(self, max_queued_length, request_data):
    try:
        print('validate_queue_length :: fetching current queue_length for auth_id : {}'.format(request_data))
        queue_type = request_data.get('queue_type', None)
        queue_id = request_data.get('queue_id', None)
        key_prefix = self._key_prefix

        allowed_queue_length = max_queued_length

        redis_key = '{}:{}:{}'.format(key_prefix, queue_type, queue_id)
        redis_conn = RedisConnection()
        redis_conn.create_redis_conn()
        key_length = redis_conn.get_key_length(redis_key)

        print("key_length :: ", key_length)

        if key_length < allowed_queue_length:
            return True
        else:
            return False
    except Exception as e:
        print('validate_queue_length :: error occurred as {}'.format(e))
        return True
