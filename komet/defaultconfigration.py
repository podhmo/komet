# -*- coding:utf-8 -*-
from zope.interface import provider
from . import interfaces as i
from .builder import (
    APISetBuilder,
    APISetCustomizer
)


@provider(i.IIndexFromRequest)
def index_from_request_default(request):
    return request.matchdict["id"]


def define_default_apiset_builder(config):
    builder = APISetBuilder(config, cutomizer=APISetCustomizer())
    config.registry.registerUtility(builder, i.IAPISetBuilder)

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


def add_apiset(config, model, name=None, **kwargs):
    builder = config.registry.getUtility(i.IAPISetBuilder)
    builder.build(model, name=name, **kwargs)


def add_custom_executor(config, model, scene, executor):
    name = model.__name__
    config.registry.adapters([scene], i.IExecutor, name, executor)


def includeme(config):
    config.include(define_default_apiset_builder)
    config.add_directive("add_apiset", add_apiset)
    config.add_directive("add_custom_executor", add_custom_executor)

    config.registry.registerUtility(index_from_request_default, i.IIndexFromRequest)
    config.registry.registerUtility(config.maybe_dotted(".repository.DefaultSQLARepository"), i.IRepository)
    config.registry.adapters.register([i.ICreate], i.IExecutor, "", config.maybe_dotted(".executors.CreateExecutor"))
    config.registry.adapters.register([i.Edit], i.Executor, "", config.maybe_dotted(".executors.EditExecutor"))
    config.registry.adapters.register([i.Delete], i.Executor, "", config.maybe_dotted(".executors.DeleteExecutor"))
