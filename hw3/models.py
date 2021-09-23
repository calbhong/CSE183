"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth, T
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()

db.define_table(
    'bird',
    Field('bird_name', requires=IS_NOT_EMPTY()),
    Field('weight','integer'),
    Field('diet', requires=IS_NOT_EMPTY()),
    Field('habitat', requires=IS_NOT_EMPTY()),
    Field('bird_count', 'integer'),
    Field('created_by', default=get_user_email),
    Field('creation_date', 'datetime', default=get_time),
)

db.bird.id.readable = db.bird.id.writable = False
db.bird.created_by.readable = db.bird.created_by.writable = False
db.bird.creation_date.readable = db.bird.creation_date.writable = False

db.bird.bird_name.label = T('Bird Species')
db.bird.weight.label = T('Weight')
db.bird.diet.label = T('Diet')
db.bird.habitat.label = T('Habitat')
db.bird.bird_count.label = T('Sightings')


db.commit()
