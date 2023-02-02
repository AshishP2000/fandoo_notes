import json
import logging

import redis
from django.conf import settings

logging.basicConfig(filename='fundoo_note.log', level=logging.DEBUG)
logger = logging.getLogger()

# redis_client = redis.Redis(**settings.REDIS_CONFIG)
# redis_client = redis.Redis(**{"host": 'localhost', "port": 6379, "db": 0})


class RedisCrud:

    redis_client = redis.Redis(**{"host": 'localhost', "port": 6379, "db": 0})

    def getter(self, key):
        """
        This function get the data of key from redis server
        """
        data = self.redis_client.get(int(key[5:6]))
        return json.loads(data) if data else {}

    def setter(self, key, value):
        """
        This function set the key value pair to the redis server
        """
        try:
            return self.redis_client.set(key, value)
        except Exception as ex:
            logger.exception(ex)
            raise Exception("Unable to set data to redis server")
