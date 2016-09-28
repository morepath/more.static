import bowerstatic
import dectate

import reg
from morepath.request import Request
from morepath.reify import reify
from morepath.app import App


class IncludeRequest(Request):

    def include(self, path_or_resource, renderer=None):
        include = self.app.bower_components.includer(self.environ)
        include(path_or_resource, renderer)


class StaticComponentsDirective(dectate.Action):
    app_class_arg = True

    def __init__(self):
        """Register a function that returns static components.
        """

    def identifier(self, app_class):
        # only one static components per app
        return ()

    def perform(self, obj, app_class):
        app_class.get_static_components = reg.methodify(obj, selfname='app')


class StaticApp(App):
    request_class = IncludeRequest

    static_components = dectate.directive(StaticComponentsDirective)

    def get_static_components(self):
        return None

    @reify
    def bower(self):
        if self.bower_components is None:
            return None
        return self.bower_components.bower

    @reify
    def bower_components(self):
        return self.get_static_components()


@StaticApp.tween_factory()
def get_bower_injector_tween(app, handler):
    if app.bower is None:
        return handler

    injector_tween = bowerstatic.InjectorTween(app.bower, handler)
    publisher_tween = bowerstatic.PublisherTween(app.bower, injector_tween)
    return publisher_tween
