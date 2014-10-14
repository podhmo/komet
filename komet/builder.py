# -*- coding:utf-8 -*-
import copy
from pyramid.decorator import reify
from .resources import resource_factory
from . import interfaces as i

"""
# how to use
def includeme(config):
    from . import interfaces as i
    builder = APISetBuilder(config, customizer=APISetCustomizer())

    # define api views
    builder.define(
        scene=i.IListing,
        customier=APISetCustomizer(
            route="%(model)s",
            path="%(model)ss/",
            view=".views.listing",
            method="GET",
            renderer="json"))

    # add api views
    builder.build(UserModel, "user", permission="operator")
    builder.build(GroupModel, "group", permission="operator")
"""


class APISetCustomizer(object):  # todo rename
    def __init__(self, route, path, view, **kwargs):
        self.route = route
        self.path = path
        self.view = view
        self.kwargs = kwargs

    def predicate(self):
        return True

    def get_route_name(self, route, name):
        return self.route % dict(model=name)

    def get_path_name(self, model, name):
        return self.path % dict(model=name)

    def get_resource_factory(self, model):
        return resource_factory(model)


class SceneManager(object):
    def __init__(self, config):
        self.config = config
        self.scenes = {}

    def register(self, scene):
        if scene:
            name = scene._InterfaceClass__attrs["name"].__name__
            self.scenes[name] = scene

    def add_custom_executor(self, scene_name, model, executor, name=""):
        scene = self.scenes[scene_name]
        self.config.registry.registerAdapter(executor, (model, scene), i.IExecutor, event=False, name=name)

    def add_custom_data_validation(self, scene_name, model, data_validation, name=""):
        scene = self.scenes[scene_name]
        self.config.registry.registerAdapter(data_validation, (model, scene), i.IDataValidation, event=False, name=name)


class APISetBuilder(object):
    def __init__(self, config, definitions=None):
        self.config = config
        self.definitions = definitions or []

    @reify
    def scene_manager(self):
        scene_manager = self.config.registry.queryUtility(i.ISceneManager)
        if scene_manager is None:
            scene_manager = SceneManager(self.config)
            self.config.registry.registerUtility(scene_manager, i.ISceneManager)
        return scene_manager

    def define(self, scene, customizer):
        self.definitions.append((scene, customizer))
        self.scene_manager.register(scene)

    def __copy__(self):
        definitions = copy.copy(self.definitions)
        return self.__class__(self.config, definitions)

    def build(self, model, name, **kwargs):
        registered = set()
        for (scene, customizer) in self.definitions:
            if customizer.predicate():
                fullroute = customizer.get_route_name(model, name)
                fullpath = customizer.get_path_name(model, name)

                if fullroute not in registered:
                    registered.add(fullroute)
                    factory = customizer.get_resource_factory(model)
                    self.config.add_route(fullroute, fullpath, factory=factory)

                kw = {}
                kw.update(customizer.kwargs)
                kw.update(kwargs)
                self.config.add_view(customizer.view, route_name=fullroute, **kw)
