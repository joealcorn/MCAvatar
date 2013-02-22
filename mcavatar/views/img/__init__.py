from flask import Blueprint

img = Blueprint('img', __name__)


@img.route('/')
def imgdex():
    return 'This subdomain will serve images from redis'
