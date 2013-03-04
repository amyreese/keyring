from flask import flash, g, redirect, request

from core import app, db, sessions, api, context, get, post, template
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

        if user is None:
            flash('Email or password incorrect.')
            return redirect(request.path + '?next={}'.format(quote_plus(next)))

        else:
            sessions.new()
            g.session['user'] = user
            return redirect(next)

    @get('/logout')
    def logout():
        sessions.destroy()
        return redirect('/')

    @get('/register', 'Register')
    @template('/register.html')
    def register_form():
        return {}

    @post('/register')
    def register():
        email = request.form['email']
        email2 = request.form['email2']

        if email != email2:
            flash('Emails do not match')
            return redirect(request.path)

        password = request.form['password']
        password2 = request.form['password2']

        if password != password2:
            flash('Passwords do not match')
            return redirect(request.path)

        users = db.query(User.id).filter(User.email == email).all()
        if len(users) > 0:
            flash('Email already registered')
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
