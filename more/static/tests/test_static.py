import os
import morepath
import more.static
from more.static.core import StaticApp
import bowerstatic
from webtest import TestApp as Client


def setup_module(module):
    morepath.disable_implicit()


def test_static():
    config = morepath.setup()
    config.scan(more.static)

    class app(StaticApp):
        testing_config = config

    @app.path(path='/')
    class Root(object):
        pass

    @app.html(model=Root)
    def default(self, request):
        request.include('jquery')
        return '<html><head></head><body></body></html>'

    bower = bowerstatic.Bower()

    components = bower.components(
        'myapp', os.path.join(os.path.dirname(__file__), 'bower_components'))

    @app.static_components()
    def get_static_includer():
        return components

    config.commit()

    c = Client(bower.wrap(app()))
    response = c.get('/')

    assert response.body == (
        b'<html><head>'
        b'<script type="text/javascript" '
        b'src="/bowerstatic/myapp/jquery/2.1.1/dist/jquery.js"></script>'
        b'</head><body></body></html>')
