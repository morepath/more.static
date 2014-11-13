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

    class App(StaticApp):
        testing_config = config

    @App.path(path='/')
    class Root(object):
        pass

    @App.html(model=Root)
    def default(self, request):
        request.include('jquery')
        return '<html><head></head><body></body></html>'

    @App.static_components()
    def get_static_includer():
        bower = bowerstatic.Bower()
        components = bower.components(
            'myapp', bowerstatic.module_relative_path('bower_components'))

        return components

    config.commit()

    c = Client(App())
    response = c.get('/')

    assert response.body == (
        b'<html><head>'
        b'<script type="text/javascript" '
        b'src="/bowerstatic/myapp/jquery/2.1.1/dist/jquery.js"></script>'
        b'</head><body></body></html>')


def test_component_url():
    config = morepath.setup()
    config.scan(more.static)

    class App(StaticApp):
        testing_config = config

    @App.path(path='/')
    class Root(object):
        pass

    @App.html(model=Root)
    def default(self, request):
        return request.app.bower_components.get_component('jquery').url()

    @App.static_components()
    def get_static_includer():
        bower = bowerstatic.Bower()
        components = bower.components(
            'myapp', bowerstatic.module_relative_path('bower_components'))

        return components

    config.commit()

    c = Client(App())
    response = c.get('/')

    assert response.body == b"/bowerstatic/myapp/jquery/2.1.1/"


def test_components_unused():
    config = morepath.setup()
    config.scan(more.static)

    class App(StaticApp):
        testing_config = config

    @App.path(path='/')
    class Root(object):
        pass

    @App.html(model=Root)
    def default(self, request):
        return '<html><head></head><body></body></html>'

    config.commit()

    c = Client(App())
    response = c.get('/')

    assert response.body == b'<html><head></head><body></body></html>'
