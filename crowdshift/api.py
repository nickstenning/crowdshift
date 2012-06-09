import json
import uuid

from flask import Blueprint, Response
from flask import request

from . import redis

def _uuid():
    return str(uuid.uuid4())

api = Blueprint('api', __name__)

def jsonify(obj, *args, **kwargs):
    res = json.dumps(obj, indent=None if request.is_xhr else 2)
    return Response(res, mimetype='application/json', *args, **kwargs)

@api.route('/')
def root():
    return jsonify({'message': 'crowdshift API'})

@api.route('/key', methods=['POST'])
def create_key():
    u = _uuid()
    if redis.set('key:%s' % u, 'OK'):
        return jsonify({ 'key': u })
    else:
        return jsonify({ 'message': 'Failed to create API key!' }, status_code=500)

