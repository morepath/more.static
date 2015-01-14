import bowerstatic
import webob

from morepath.request import Request
from morepath.reify import reify
from morepath.app import App
from reg import dispatch
from morepath import Directive


@dispatch()
def get_static_components():
    return None


class IncludeRequest(Request):

    def include(self, path_or_resource, renderer=None):
        include = self.app.bower_components.includer(self.environ)
        include(path_or_resource, renderer)


class StaticApp(App):
    request_class = IncludeRequest

    @reify
    def bower(self):
        if self.bower_components is None:
            return None
        return self.bower_components.bower

    @reify
    def bower_components(self):
        return get_static_components(lookup=self.lookup)


@StaticApp.directive('static_components')
class StaticComponentsDirective(Directive):
    def identifier(self, app):
        # only one static components per app
        return ()

    def perform(self, registry, obj):
        registry.register_function(get_static_components, obj)


@StaticApp.tween_factory()
def get_bower_injector_tween(app, handler):
    if app.bower is None:
        return handler

    injector_tween = bowerstatic.InjectorTween(app.bower, handler)
    publisher_tween = bowerstatic.PublisherTween(app.bower, injector_tween)
    return publisher_tween

