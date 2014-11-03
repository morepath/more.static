from morepath.request import Request
from morepath.reify import reify
from morepath.app import App
from reg import generic
from morepath import Directive


@generic
def get_static_components():
    raise NotImplementedError()


class IncludeRequest(Request):
    @reify
    def static_components(self):
        return get_static_components(lookup=self.lookup)

    def include(self, path_or_resource):
        include = self.static_components.includer(self.environ)
        include(path_or_resource)


class StaticApp(App):
    request_class = IncludeRequest


@StaticApp.directive('static_components')
class StaticComponentsDirective(Directive):
    def identifier(self, app):
        # only one static components per app
        return ()

    def perform(self, registry, obj):
        registry.register(get_static_components, (), obj)
