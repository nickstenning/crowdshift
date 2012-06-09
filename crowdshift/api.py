import json

from flask import Blueprint, Response
from flask import request

api = Blueprint('api', __name__)

def jsonify(obj, *args, **kwargs):
    res = json.dumps(obj, indent=None if request.is_xhr else 2)
    return Response(res, mimetype='application/json', *args, **kwargs)

@api.route('/')
def root():
    return jsonify({'message': 'crowdshift API'})
