from redis import RedisConnection
MAX_ALLOWED_HOURS = 6


def max_queue_length(self, account_cps):
    try:
        print('max_queue_length :: fetching queue_length, max allowed is 6 hours.')
        return (account_cps * 60 * 60) * MAX_ALLOWED_HOURS
    except Exception as e:
        print('max_queue_length :: error occurred as {}'.format(e))
        return 0


def validate_queue_length(self, request_data):
    try:
        print('validate_queue_length :: fetching current queue_length for auth_id : {}'.format(request_data))
        account_cps = request_data.get('account_cps', None)
        queue_type = request_data.get('queue_type', None)
        queue_id = request_data.get('queue_id', None)
        key_prefix = self._key_prefix

        if account_cps is not None:
            account_cps = int(account_cps)
        allowed_queue_length = self.max_queue_length(self, account_cps)

        redis_key = '{}:{}:{}'.format(key_prefix, queue_type, queue_id)
        redis_conn = RedisConnection()
        redis_conn.create_redis_conn()
        key_length = redis_conn.get_key_length(redis_key)

        if key_length < allowed_queue_length:
            return True
        else:
            return False
    except Exception as e:
        print('validate_queue_length :: error occurred as {}'.format(e))
        return True
