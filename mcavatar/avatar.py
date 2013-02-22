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
    helm_box = (40, 8, 48, 16)
    expiry = config.IMG_CACHE_TIMEOUT

    def __init__(self, username, size=48, helmet='h'):
        self.username = username
        self.size = (size, size)
        self.helmet = True if helmet == 'h' else False
        self.url = base_url.format(username)
        self.key = '{0}_{1}_{2}'.format(size, helmet, username)

        if username.lower() == 'char':
            # Ensure the case is correct
            # and set expiry to one week
            self.username = 'char'
            self.expiry = 60 * 60 * 24 * 7

    def skin(self):
        r = requests.get(self.url)
        if r.status_code == 403:
            # Probably not the best error to raise,
            # but at least it won't be raised by
            # something else
            raise NotImplementedError

        return StringIO(r.content)

    def render(self):
        skin = Image.open(self.skin())
        head = skin.copy().crop(self.box)

        if self.helmet:
            helm = skin.crop(self.helm_box)
            head = head.convert('RGBA')
            helm = helm.convert('RGBA')
            head.paste(helm, None, helm)

        head = head.resize(self.size)

        out = StringIO()
        head.save(out, 'png')

        redis.setex(self.key, out.getvalue(), self.expiry)
        return out.getvalue()
