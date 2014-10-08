# -*- coding:utf-8 -*-
import copy
from .resources import resource_factory

"""
# how to use
def includeme(config):
    from . import interfaces as i
    builder = APISetBuilder(config, cutomizer=APISetCustomizer())

    # define api views
    builder.define(
        route="%(model)s",
        scene=i.IListing,
        path="%(model)ss/",
        view=".views.listing",
        method="GET",
        renderer="json")
    builder.define(
        route="%(model)s",
        scene=i.ICreate,
        path="%(model)ss/",
        view=".views.create",
        method="POST",
        renderer="json")
    builder.define(
        route="%(model)s.unit",
        scene=i.IShow,
        path="%(model)ss/{id}",
        view=".views.show",
        method="GET",
        renderer="json")
    builder.define(
        route="%(model)s.unit",
        scene=i.IEdit,
        path="%(model)ss/{id}",
        view=".views.edit",
        method="PUT",
        renderer="json")
    builder.define(
        route="%(model)s.unit",
        scene=i.IDelete,
        path="%(model)ss/{id}",
        view=".views.delete",
        method="DELETE",
        renderer="json")

    # add api views
    builder.build(UserModel, "user", permission="operator")
    builder.build(GroupModel, "group", permission="operator")
"""


class APISetCustomizer(object):  # todo rename
    def get_route_name(self, route, name):
        return route % dict(model=name)

    def get_path_name(self, path, name):
        return path % dict(model=name)

    def get_resource_factory(self, model):
        return resource_factory(model)

    def get_model_name(self, model):
        return model.__name__.lower()


class APISetBuilder(object):
    def __init__(self, config, customizer=None, definitions=None):
        self.config = config
        self.customizer = customizer or APISetCustomizer()
        self.definitions = definitions or {}

    def define(self, route, scene, path, view, **kwargs):
        self.definitions[(route, scene)] = (path, view, kwargs)

    def __copy__(self):
        definitions = copy.copy(self.definitions)
        return self.__class__(self.config, self.customizer, definitions)

    def build(self, model, name=None, **kwargs):
        if name is None:
            name = self.customizer.get_model_name(model)

        registered = set()
        for (route, scene), (path, view, new_kwargs) in self.definitions.items():
            fullroute = self.customizer.get_route_name(route, name)
            fullpath = self.customizer.get_path_name(path, name)

            if fullroute not in registered:
                registered.add(fullroute)
                factory = self.customizer.get_resource_factory(model)
                self.config.add_route(fullroute, fullpath, factory=factory)

            kw = {}
            kw.update(new_kwargs)
            kw.update(kwargs)
            self.config.add_view(view, route_name=fullroute, **kw)

