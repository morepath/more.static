from morepath.request import Request
from morepath.app import App
from reg import generic
from morepath import Directive


@generic
def get_static_components():
    raise NotImplementedError()


class StaticApp(App):
    def request(self, environ):
        request = IncludeRequest(environ)
        request.lookup = self.lookup
        return request


@StaticApp.directive('static_components')
class StaticComponentsDirective(Directive):
    def identifier(self, app):
        # only one static components per app
        return ()

    def perform(self, registry, obj):
        registry.register(get_static_components, (), obj)


class IncludeRequest(Request):
    def include(self, path_or_resource):
        components = get_static_components(lookup=self.lookup)
        include = components.includer(self.environ)
        include(path_or_resource)
