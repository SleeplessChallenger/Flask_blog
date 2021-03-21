from flask import Blueprint

api = Blueprint('api', __name__)

# from . import authentication, comments, errors, posts, users
from . import authentication, errors, users, posts
# we import them below so as to bypass circular error
