from datetime import datetime
import json
import uuid as uuidlib

from flask import request, Response

def jsonify(obj, *args, **kwargs):
    res = json.dumps(obj, indent=None if request.is_xhr else 2)
    return Response(res, mimetype='application/json', *args, **kwargs)

def uuid():
    return str(uuidlib.uuid4())

def date_to_timestamp(date):
    d = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
    return d.strftime('%s')

def timestamp_to_date(timestamp):
    return datetime.fromtimestamp(int(timestamp))
