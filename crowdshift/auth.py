from decorator import decorator

from flask import g

from . import rc
from .util import jsonify

@decorator
def require_key(func, *args, **kwargs):
    """

    Decorator: ensure the bearer API key is supplied.

    """
    fail = jsonify({'message': 'Valid API key required!'}, status=401)

    if g.auth is None:
        return fail

    typ, val = g.auth

    if typ != 'bearer':
        return fail

    if rc.get('key:%s' % val) != 'OK':
        return fail

    return func(*args, **kwargs)
