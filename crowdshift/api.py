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

    rc.setex('token:%s' % tok, 86400, cid)
    rc.zadd('event:%s:commitments' % eid, start_ts, cid)
    rc.set('commitment:%s:start' % cid, start_ts)
    rc.set('commitment:%s:end'   % cid, end_ts)

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


@api.route('/event/<eid>/attendance')
def get_attendance(eid):
    try:
        start = utc8601_to_date(request.args['start'])
    except (KeyError, ValueError):
        start = datetime.datetime.utcnow()

    try:
        end = utc8601_to_date(request.args['end'])
    except (KeyError, ValueError):
        end = start + datetime.timedelta(days=1)

    try:
        resolution = int(request.args['resolution'])
    except (KeyError, ValueError):
        resolution = 3600

    start_ts = start.strftime('%s')
    end_ts = end.strftime('%s')

    attendance = [[x, 0] for x in xrange(int(start_ts), int(end_ts), resolution)]

    # find all commitments starting in range [start_ts, end_ts)
    for cid, cstart in rc.zrangebyscore('event:%s:commitments' % eid, start_ts, '(%s' % end_ts, withscores=True):
        # we have cstart, but we need to get cend
        cend = rc.get('commitment:%s:end' % cid)

        # walk through attendance, and for each attendance entry within time range,
        # increment attendance numbers
        for entry in attendance:
            if int(cstart) <= entry[0] < int(cend):
                entry[1] += 1

    attendance = [[timestamp_to_date(x[0]).isoformat(), x[1]] for x in attendance]

    return jsonify({
        'start': start.isoformat(),
        'end': end.isoformat(),
        'resolution': resolution,
        'attendance': attendance
    })
