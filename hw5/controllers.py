"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email, get_user, get_name

url_signer = URLSigner(session)

@action('index')
@action.uses(db, auth.user, 'index.html')
def index():
    return dict(
        # COMPLETE: return here any signed URLs you need.
        load_posts_url = URL('load_posts', signer=url_signer),
        add_post_url = URL('add_post', signer=url_signer),
        delete_post_url = URL('delete_post', signer=url_signer),
        get_rating_url = URL('get_rating', signer=url_signer),
        set_rating_url = URL('set_rating', signer=url_signer),  
    )

@action('load_posts')
@action.uses(url_signer.verify(), db, auth.user)
def load_posts():
    rows = db(db.posts).select().as_list()
    user = get_user()
    return dict(rows=rows,user=user)

@action('add_post', method="POST")
@action.uses(url_signer.verify(),db)
def add_post():
    name = get_name()
    email = get_user_email()
    #let's check if the name has changed at all
    #add post to db 
    id = db.posts.insert(
        author_name = name,
        post_text = request.json.get('post_text')
    )
    return dict(id=id,name=name,email=email)

@action('delete_post')
@action.uses(url_signer.verify(),db,auth.user)
def delete_post():
    id = request.params.get('id')
    auth_id = request.params.get('auth_id')
    assert id is not None
    if int(auth_id) == int(get_user()):
        db(db.posts.id == id).delete()
    return("ok")

@action('get_rating')
@action.uses(url_signer.verify(),db,auth.user)
def get_rating():
    post_id = request.params.get('post_id')
    row = db((db.ratings.post_id == post_id) &
            (db.ratings.rater == get_user())).select().first()
    rating = row.rating if row is not None else 0

    return dict(rating = rating)

@action('set_rating', method='POST')
@action.uses(url_signer.verify(), db, auth.user)
def set_rating():
    rating_post_id = request.json.get('rating_post_id')
    rating_value = request.json.get('rating_value')
    assert rating_post_id is not None and rating_value is not None
    db.ratings.update_or_insert(
        ((db.ratings.post_id == rating_post_id) & (db.ratings.rater == get_user())),
        post_id = rating_post_id,
        rater = get_user(),
        rating = rating_value
    )
    return("ok")