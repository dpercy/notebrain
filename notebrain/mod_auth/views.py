
from flask import Blueprint, abort, g, redirect, request, session
from flask.ext import openid
from flask.ext.mako import render_template

from notebrain import app

from .models import User

mod_auth = Blueprint('auth', __name__, url_prefix='/auth', template_folder='../templates/auth')
oid = openid.OpenID(app, './openid-tmp', safe_roots=[])

@app.before_request
def lookup_current_user():
    g.user = None
    if 'openid' in session:
        openid = session['openid']
        g.user = User.objects(openid=openid).get()

@mod_auth.route('/logout', methods=['GET'])
def logout():
    session.pop('openid', None)
    return redirect(oid.get_next_url())

@mod_auth.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None:
        return redirect(oid.get_next_url())
    if request.method == 'POST':
        oid_url = request.form.get('openid_url')
        if oid_url:
            return oid.try_login(
                oid_url,
                ask_for=['email', 'nickname'],
                ask_for_optional=['fullname'],
            )
    err = oid.fetch_error()
    if err:
        # TODO should this go to a log, or to the user?
        print 'err', repr(err), err
    return render_template(
        'login.html',
        next = oid.get_next_url(),
        error = err,
        providers = openid.COMMON_PROVIDERS,
        debug = app.debug,
        debug_users = User.objects if app.debug else [],
    )

@mod_auth.route('/fake_login', methods=['POST'])
def fake_login():
    """
    Automatically log in as a particular user.
    Only works in debug mode; useful for offline development.
    """
    if not app.debug:
        abort(404)
    session['openid'] = request.form['user']
    return redirect('/')

@oid.after_login
def create_or_login(resp):
    """This is called when login with OpenID succeeded and it's not
    necessary to figure out if this is the users's first login or not.
    This function has to redirect otherwise the user will be presented
    with a terrible URL which we certainly don't want.
    """
    session['openid'] = resp.identity_url
    if 'pape' in resp.extensions:
        pape_resp = resp.extensions['pape']
        session['auth_time'] = pape_resp.auth_time
    user = User.get_or_create(
        openid=resp.identity_url,
        fullname=resp.fullname,
        nickname=resp.nickname,
        image_url=resp.image,
        email=resp.email,
    )
    assert user is not None
    assert isinstance(user, User)

    g.user = user
    return redirect(oid.get_next_url())
