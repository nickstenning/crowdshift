from flask import Blueprint, g

from . import rc
from .auth import require_key
from .util import jsonify, uuid

api = Blueprint('api', __name__)

@api.route('/')
def root():
    return jsonify({'message': 'crowdshift API'})

@api.route('/key', methods=['POST'])
def create_key():
    u = uuid()

    assert rc.setnx('key:%s' % u, 'OK')
    return jsonify({'key': u})

@api.route('/event', methods=['POST'])
@require_key
def create_event():
    _, key = g.auth
    u = uuid()

    assert rc.setnx('event:%s:owner' % u, key)
    return jsonify({'id': u})
