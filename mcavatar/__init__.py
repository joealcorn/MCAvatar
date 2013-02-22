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
