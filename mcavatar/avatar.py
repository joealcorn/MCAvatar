from cStringIO import StringIO

from redis import Redis
from PIL import Image
import requests

import config

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB
)

base_url = 'http://s3.amazonaws.com/MinecraftSkins/{0}.png'


class Avatar(object):

    box = (8, 8, 16, 16)
    hat_box = (40, 8, 48, 16)
    expiry = config.IMG_CACHE_TIMEOUT

    def __init__(self, username, size=48, helmet=True):
        self.username = username
        self.size = (size, size)
        self.helmet = helmet
        self.url = base_url.format(username)
        self.key = '{0}_{1}'.format(size, username)

    def skin(self):
        r = requests.get(self.url)
        if r.status_code != 200:
            raise Exception

        return StringIO(r.content)

    def render(self):
        skin = Image.open(self.skin())
        head = skin.crop(self.box)
        head = head.resize(self.size)

        out = StringIO()
        head.save(out, 'png')

        redis.setex(self.key, out.getvalue(), self.expiry)
        return out.getvalue()
