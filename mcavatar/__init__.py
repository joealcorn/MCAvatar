from redis import Redis
from flask import Flask, g

app = Flask(__name__)
app.config.from_pyfile('config.py')

_redis = Redis(
    host=app.config['REDIS_HOST'],
    port=app.config['REDIS_PORT'],
    db=app.config['REDIS_DB']
)

from mcavatar.views.public import public
from mcavatar.views.img import img

app.register_blueprint(public)
app.register_blueprint(img, subdomain='i')


@app.before_request
def set_db():
    g.redis = _redis


@app.teardown_request
def incr_requests(ex):
    g.redis.incr('total_requests')


@app.template_filter('time')
def seconds_to_hrt(seconds):
    hours = seconds / 3600
    minutes = seconds / 60 - hours * 60

    if minutes != 0:
        return '{0}h {1}m'.format(hours, minutes)
    else:
        return '{0}h'.format(hours)
