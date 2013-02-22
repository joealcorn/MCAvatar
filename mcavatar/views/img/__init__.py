from functools import wraps
import re

from flask import Blueprint, g, make_response

from mcavatar import app
from mcavatar.avatar import Avatar

img = Blueprint('img', __name__)


username_re = re.compile('([A-Z_0-9]){2,16}', re.I)
d_size = app.config.get('DEFAULT_IMG_SIZE', 48)
m_size = app.config.get('MAX_IMG_SIZE', 999)
l_size = app.config.get('LOW_IMG_SIZE', 16)


def valid_user(user):
    if len(user) > 16 or not username_re.match(user):
        return False
    else:
        return True


def validate(func):
    @wraps(func)
    def wrapped(user, size=d_size, *a, **kw):
        if not valid_user(user):
            user = 'char'

        if size > m_size:
            size = m_size
        elif size < l_size:
            size = l_size

        return func(user, size, *a, **kw)
    return wrapped


def image_response(user, size=d_size):
    key = '{0}_{1}'.format(size, user)
    img = g.redis.get(key)
    if img is None:
        try:
            a = Avatar(user, size=size)
            img = a.render()
        except NotImplementedError:
            return image_response('char', size)

    response = make_response(img)
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Disposition'] = 'inline'

    return response


@img.route('/a/<user>/<int:size>')
@img.route('/a/<user>/<int:size>.png')
@img.route('/a/<user>')
@img.route('/a/<user>.png')
@validate
def avatar(user, size=d_size):
    return image_response(user, size)


@img.route('/a/refresh/<user>')
def refresh(user):
    if not valid_user(user):
        return 'bad user'

    keys = g.redis.keys('*_{0}'.format(user))
    g.redis.delete(*keys)
    return 'ok'
