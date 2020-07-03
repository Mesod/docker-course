import os

from flask import Flask
from flask_restful import Resource, Api
import redis

ENABLE_REDIS_DEFAULT = 'false'
REDIS_HOST_DEFAULT = 'localhost'
DEBUG_MODE = os.getenv('DEVELOPMENT_MODE', 'true').lower() == 'true'
REDIS_HOST = os.getenv('REDIS_HOST', REDIS_HOST_DEFAULT)
ENABLE_REDIS = os.getenv('ENABLE_REDIS', ENABLE_REDIS_DEFAULT).lower() == 'true'
APP_PORT = 8000

print(ENABLE_REDIS)

app = Flask(__name__)
api = Api(app)

redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0)


class HelloWorld(Resource):
    def get(self):
        if ENABLE_REDIS:
            request_count = redis_client.get('request_count')
            if request_count is None:
                request_count = 1
            else:
                request_count = 1 + int(request_count)
            redis_client.set('request_count', request_count)
        else:
            request_count = 'no redis is available'

        return {'hello': 'world', 'reqeust_count': request_count}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=DEBUG_MODE, host='0.0.0.0', port=APP_PORT)