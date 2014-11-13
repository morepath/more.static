import bowerstatic

from morepath.request import Request
from morepath.reify import reify
from morepath.app import App
from reg import dispatch
from morepath import Directive


@dispatch()
def get_static_components():
    raise NotImplementedError()


class IncludeRequest(Request):

    def include(self, path_or_resource):
        include = self.app.bower_components.includer(self.environ)
        include(path_or_resource)


class StaticApp(App):
    request_class = IncludeRequest

    @reify
    def bower(self):
        return bowerstatic.Bower()

    @reify
    def bower_components(self):
        return get_static_components(lookup=self.lookup)

    @reify
    def bower_publisher(self):
        return bowerstatic.publisher.Publisher(self.bower, None)

    @reify
    def bower_injector(self):
        return bowerstatic.injector.Injector(self.bower, None)


@StaticApp.directive('static_components')
class StaticComponentsDirective(Directive):
    def identifier(self, app):
        # only one static components per app
        return ()

    def perform(self, registry, obj):
        registry.register_function(get_static_components, obj)


@StaticApp.tween_factory()
def get_bower_injector_tween(app, handler):
    def bower_injector_tween(request):
        response = handler(request)
        response = request.app.bower_injector.inject(request, response)
        response = request.app.bower_publisher.publish(request, response)
        return response
    return bower_injector_tween
