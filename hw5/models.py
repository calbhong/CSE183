"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()

def get_user():
    return auth.current_user.get('id') if auth.current_user else None

def get_name():
    r = db(db.auth_user.email == get_user_email()).select().first()
    name = r.first_name + " " + r.last_name if r is not None else "Unknown"
    return name


### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later



db.define_table('posts',
                Field('auth_id', 'reference auth_user', default=get_user),
                Field('email',default=get_user_email),
                Field('author_name'),
                Field('post_text', requires=IS_NOT_EMPTY())
)

db.define_table('ratings',
                Field('post_id', 'reference posts'),
                Field('rater', 'reference auth_user', default=get_user),
                Field('rating', 'integer',default=0)
)

db.commit()
