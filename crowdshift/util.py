from datetime import datetime
import json
import uuid as uuidlib

from flask import request, Response

def jsonify(obj, *args, **kwargs):
    res = json.dumps(obj, indent=None if request.is_xhr else 2)
    if 'callback' in request.args:
        return Response('%s(%s);' % (request.args['callback'], res), mimetype='text/javascript', *args, **kwargs)
    else:
        return Response(res, mimetype='application/json', *args, **kwargs)

def uuid():
    return str(uuidlib.uuid4())


def utc8601_to_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')

def timestamp_to_date(timestamp_str):
    return datetime.fromtimestamp(int(timestamp_str))
