from flask import g

from core import get, api, template

@get('/lipsum', 'Lorem Ipsum')
@template('lipsum.html')
def lipsum():
    return {}

@get('/session')
@template('api.html')
def session():
    return {'content': str(g.session)}
