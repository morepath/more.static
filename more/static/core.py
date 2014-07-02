from morepath.request import Request
from morepath.app import App
from reg import generic
from morepath.config import Directive


@generic
def get_static_includer(request):
    raise NotImplementedError()


class StaticIncluderDirective(Directive):
    def identifier(self, app):
        # only one static includer per app
        return ()

    def perform(self, app, obj):
        app.register(get_static_includer, (StaticIncluderRequest,), obj)


class StaticIncluderRequest(Request):
    def include(self, path_or_resource):
        include = get_static_includer(self, lookup=self.lookup)
        include(path_or_resource)


class StaticApp(App):
    def request(self, environ):
        request = StaticIncluderRequest(environ)
        request.lookup = self.lookup
        return request

def method(self, *args, **kw):
    return StaticIncluderDirective(self, *args, **kw)

StaticApp.static_includer = method

