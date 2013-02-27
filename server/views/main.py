from core import app, get, api, template
from core.routing import api_help

@get('/', 'Hello World!')
@template('page.html')
def hello():
    return {}

@get(app.config['API_ROOT'], 'API Listing')
@template('api.html')
def api_index():
    """Returns a plain text listing of API methods, parameters, and descriptions."""
    output = ''
    for url in sorted(api_help.iterkeys()):
        output += api_help[url]

    return {'content': output}


