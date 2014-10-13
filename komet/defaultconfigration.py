# -*- coding:utf-8 -*-
from zope.interface import provider
from . import interfaces as i
from .builder import (
    APISetBuilder,
    APISetCustomizer
)
from .renderers import ModelRendererFactory


@provider(i.IIndexFromRequest)
def index_from_request_default(request):
    return request.matchdict["id"]


def define_default_apiset_builder(config):
    builder = APISetBuilder(config, customizer=APISetCustomizer())
    config.registry.registerUtility(builder, i.IAPISetBuilder)

    # define api views
    builder.define(
        route="%(model)s",
        scene=i.IListing,
        path="%(model)ss/",
        view=".views.listing",
        request_method="GET",
        renderer="json")
    builder.define(
        route="%(model)s",
        scene=i.ICreate,
        path="%(model)ss/",
        view=".views.create",
        request_method="POST",
        renderer="json")
    builder.define(
        route="%(model)s.unit",
        scene=i.IShow,
        path="%(model)ss/{id}/",
        view=".views.show",
        request_method="GET",
        renderer="json")
    builder.define(
        route="%(model)s.unit",
        scene=i.IEdit,
        path="%(model)ss/{id}/",
        view=".views.edit",
        request_method="PUT",
        renderer="json")
    builder.define(
        route="%(model)s.unit",
        scene=i.IDelete,
        path="%(model)ss/{id}/",
        view=".views.delete",
        request_method="DELETE",
        renderer="json")
    builder.define(
        route="%(model)s.schema",
        scene=None,
        path="%(model)ss/schema",
        view=".views.schema",
        request_method="GET",
        renderer="json")


def add_apiset(config, model, name=None, **kwargs):
    builder = config.registry.getUtility(i.IAPISetBuilder)
    builder.build(model, name=name, **kwargs)


def add_custom_executor(config, model, scene, executor):
    name = model.__name__
    config.registry.adapters([scene], i.IExecutor, name, executor)


def add_dbsession(config, session):
    config.registry.registerUtility(session, i.IDBSession)


def add_model_renderer(config, Base):
    from pyramid.renderers import JSON
    renderer = JSON()
    factory = ModelRendererFactory(renderer)
    config.add_renderer("json", factory(Base))


def includeme(config):
    config.include(define_default_apiset_builder)
    config.add_directive("add_komet_apiset", add_apiset)
    config.add_directive("add_komet_dbsession", add_dbsession)
    config.add_directive("add_komet_custom_executor", add_custom_executor)
    config.add_directive("add_komet_model_renderer", add_model_renderer)

    config.registry.registerUtility(index_from_request_default, i.IIndexFromRequest)
    config.registry.registerUtility(config.maybe_dotted(".repository.DefaultSQLARepository"), i.IRepository)
    config.registry.adapters.register([i.ICreate], i.IExecutor, "", config.maybe_dotted(".executors.CreateExecutor"))
    config.registry.adapters.register([i.IEdit], i.IExecutor, "", config.maybe_dotted(".executors.EditExecutor"))
    config.registry.adapters.register([i.IDelete], i.IExecutor, "", config.maybe_dotted(".executors.DeleteExecutor"))

    # jsonschema
    config.registry.adapters.register([i.ICreate], i.IValidation, "", config.maybe_dotted(".executors.create_jsonschema_validation"))
    config.registry.adapters.register([i.IEdit], i.IValidation, "", config.maybe_dotted(".executors.edit_jsonschema_validation"))
    config.registry.adapters.register([i.IDelete], i.IValidation, "", config.maybe_dotted(".executors.delete_jsonschema_validation"))

    from alchemyjsonschema import SingleModelWalker, SchemaFactory
    factory = SchemaFactory(SingleModelWalker)
    config.registry.registerUtility(factory, i.ISchemaFactory)

