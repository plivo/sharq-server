import configparser
import argparse
import os
import redis


class RedisConnection:
    def __init__(self):
        parser = argparse.ArgumentParser(description='SharQ Server.')
        parser.add_argument('-c', '--config', action='store', required=True,
                            help='Absolute path of the SharQ configuration file.',
                            dest='sharq_config')
        args = parser.parse_args()
        self.config_file = os.path.abspath(args.sharq_config)
        self.redis_conn = None

    def create_redis_conn(self):
        try:
            # Read config file
            config = configparser.SafeConfigParser()
            config.read(self.config_file)

            # Get Redis details from config file
            redis_config = config['redis']
            redis_port = int(redis_config.get('port', None))
            redis_host = redis_config.get('host', None)
            redis_pass = redis_config.get('password', None)

            # Create Redis connection
            self.redis_conn = redis.Redis(host=redis_host, port=redis_port, password=redis_pass)
            self.redis_conn.ping()
            return self.redis_conn
        except Exception as e:
            print('create_redis_conn :: error occurred as {}'.format(e))

    def get_key_length(self, key):
        try:
            return self.redis_conn.llen(key)
        except Exception as e:
            print('get_key_length :: error occurred as {}'.format(e))
