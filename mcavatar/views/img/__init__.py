from functools import wraps
import re

from flask import Blueprint, g, make_response

from mcavatar import app
from mcavatar.avatar import Avatar

img = Blueprint('img', __name__)


username_re = re.compile('([A-Z_0-9]){2,16}', re.I)
d_size = app.config.get('DEFAULT_IMG_SIZE', 48)
max_size = app.config.get('MAX_IMG_SIZE', 999)
min_size = app.config.get('MIN_IMG_SIZE', 16)


def valid_user(user):
    if len(user) > 16 or not username_re.match(user):
        return False
    else:
        return True


def validate(func):
    @wraps(func)
    def wrapped(helm, user, size=d_size, *a, **kw):
        if not valid_user(user):
            user = 'char'

        if size > max_size:
            size = max_size
        elif size < min_size:
            size = min_size

        helm = helm.lower()
        if helm not in ('h', 'f'):
            helm = 'h'

        return func(helm, user, size, *a, **kw)
    return wrapped


def image_response(user, size=d_size, helmet='h'):
    key = '{0}_{1}_{2}'.format(size, helmet, user)
    img = g.redis.get(key)
    if img is None:
        try:
            a = Avatar(user, size, helmet)
            img = a.render()
        except:
            return image_response('char', size)

    response = make_response(img)
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Disposition'] = 'inline'

    return response


@img.route('/<helm>/<user>/<int:size>')
@img.route('/<helm>/<user>/<int:size>.png')
@img.route('/<helm>/<user>')
@img.route('/<helm>/<user>.png')
@validate
def avatar(helm, user, size=d_size):
    return image_response(user, size, helm)


@img.route('/update/<user>')
def update(user):
    if not valid_user(user):
        return 'bad user'

    keys = g.redis.keys('*_{0}'.format(user))
    if keys != []:
        g.redis.delete(*keys)
    return 'ok'
