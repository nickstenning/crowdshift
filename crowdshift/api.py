import datetime
from flask import Blueprint, g, request

from . import rc
from .auth import require_key
from .util import jsonify, uuid, utc8601_to_date, timestamp_to_date

api = Blueprint('api', __name__)

@api.route('/')
def root():
    return jsonify({'message': 'crowdshift API'})

@api.route('/key', methods=['POST'])
def create_key():
    uid = uuid()

    assert rc.setnx('key:%s' % uid, 'OK')
    return jsonify({'key': uid}, status=201)

@api.route('/event', methods=['POST'])
@require_key
def create_event():
    _, key = g.auth
    uid = uuid()

    assert rc.setnx('event:%s:owner' % uid, key)
    return jsonify({'id': uid}, status=201)

@api.route('/event/<eid>/commitment', methods=['POST'])
@require_key
def create_commitment(eid):
    _, key = g.auth

    if rc.get('event:%s:owner' % eid) != key:
        return jsonify({'message': "This ain't your event, buster!"}, status=401)

    try:
        start = utc8601_to_date(request.form['start'])
    except KeyError:
        start = datetime.datetime.utcnow()
    except ValueError:
        return jsonify({'message': "'%s' is an invalid start time!" % request.form['start']}, status=400)

    try:
        end = utc8601_to_date(request.form['end'])
    except KeyError:
        end = start + datetime.timedelta(hours=4)
    except ValueError:
        return jsonify({'message': "'%s' is an invalid end time!" % request.form['end']}, status=400)

    if end < start:
        return jsonify({'message': "End time should be before start time!"}, status=400)

    # If we got this far, we should have two sane times, so create the entry:

    start_ts = start.strftime('%s')
    end_ts = end.strftime('%s')

    tok = uuid()
    cid = uuid()

    rc.setex('token:%s', 86400, tok)
    rc.zadd('event:%s:commitments' % eid, start_ts, cid)
    rc.set('commitment:%s:start' % cid, start_ts)
    rc.set('commitment:%s:end'   % cid, end_ts)
    rc.set('commitment:%s:token' % cid, tok)

    return jsonify({
        "id": cid,
        "token": tok,
        "start": start.isoformat(),
        "end": end.isoformat()
    }, status=201)

@api.route('/event/<eid>/commitment/<cid>')
def get_commitment(eid, cid):
    if not rc.zscore('event:%s:commitments' % eid, cid):
        return jsonify({'message': 'Commitment not found!'}, status=404)

    start = rc.get('commitment:%s:start' % cid)
    end = rc.get('commitment:%s:end' % cid)

    return jsonify({
        "id": cid,
        "start": timestamp_to_date(start).isoformat(),
        "end": timestamp_to_date(end).isoformat()
    })


