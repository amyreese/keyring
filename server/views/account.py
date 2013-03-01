import uuid
from urllib import quote_plus

from flask import flash, g, redirect, request, session

from core import app, db, mc, mcdict, api, context, get, post, template
from models import User

with context('/account'):

    @get('/login', 'Login')
    @template('/login.html')
    def login_form(next=None):
        if next is None:
            next = request.referrer

        return {'next': next}

    @post('/login')
    def login():
        next = '/'
        if 'next' in request.form:
            next = request.form['next']
        else:
            next = '/'

        email = request.form['email']
        password = request.form['password']

        user = User.authenticate(email, password)
        app.logger.debug('authenticate() result: {}'.format(user))

        if user is None:
            flash('Email or password incorrect.')
            return redirect(request.path + '?next={}'.format(quote_plus(next)))

        else:
            g.session['user'] = user
            return redirect(next)

    @get('/logout')
    def logout():
        if g.user.id is not None:
            del(g.session['user'])

        return redirect('/')

    @get('/register', 'Register')
    @template('/register.html')
    def register_form():
        return {}

    @post('/register')
    def register():
        email = request.form['email']
        email = request.form['email']

        password = request.form['password']
        password2 = request.form['password2']

        users = db.query(User.id).filter(User.email == email).all()
        if len(users) > 0:
            flash('Email already registered')
            return redirect(request.path)

        if password != password2:
            flash('Passwords do not match')
            return redirect(request.path)

        user = User(email, password)
        db.add(user)
        db.commit()

        g.session['user'] = user

        return redirect('/')

    @get('', 'Account')
    @template('/account.html')
    def user_profile():
        return {'content': g.session['user'].id}

@app.before_request
def user_before_request():
    """Pull user data from session if found, or use anonymous user otherwise."""
    g.session = None

    if 'session-key' in session:
        session_key = session['session-key']
        if mc.get(session_key) is not None:
            g.session = mcdict(session_key)

    if g.session is None:
        session_key = 'session-' + uuid.uuid4().hex
        g.session = mcdict(session_key)
        session['session-key'] = session_key

    if 'user' not in g.session:
        g.session['user'] = User()
    g.user = g.session['user']

    if g.user.id == None:
        g.account_links = [
            {'href': '/account/register', 'title': 'Register'},
            {'href': '/account/login', 'title': 'Login'},
        ]
    else:
        g.account_links = [
            {'href': '/account', 'title': g.user.email},
            {'href': '/account/logout', 'title': 'Logout'},
        ]
