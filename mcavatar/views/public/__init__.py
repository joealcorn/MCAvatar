from flask import Blueprint, render_template

public = Blueprint('public', __name__)


@public.route('/')
def index():
    return render_template('index.html')
