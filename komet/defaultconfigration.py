# -*- coding:utf-8 -*-
from zope.interface import provider
from . import interfaces as i
from .builder import (
    APISetBuilder,
    APISetCustomizer,
    IndirectAPISetCustomizer
)
from .renderers import ModelRendererFactory


@provider(i.IRequestParser)
class IndexFromRequest(object):
    def __init__(self, request):
        self.request = request

    def get_index(self):
        return self.request.matchdict["id"]

    def get_child_index(self):
        return self.request.matchdict["child_id"]


def define_default_apiset_builder(config):
    builder = APISetBuilder(config)
    config.registry.registerUtility(builder, i.IAPISetBuilder)

    # define api views
    builder.define(
        None,
        APISetCustomizer(
            route="%(model)s.schema",
            path="%(model)s/schema/",
            view=".views.schema",
            request_method="GET",
            renderer="json"),
        "getting schema information of %(model)s"
    )

    builder.define(
        i.IListing,
        APISetCustomizer(
            route="%(model)s",
            path="%(model)s/",
            view=".views.listing",
            request_method="GET",
            renderer="json"),
        "list %(model)s objects"
    )

    builder.define(
        i.ICreate,
        APISetCustomizer(
            route="%(model)s",
            path="%(model)s/",
            view=".views.create",
            request_method="POST",
            renderer="json"),
        "create %(model)s object"
    ),

    builder.define(
        i.IShow,
        APISetCustomizer(
            route="%(model)s.unit",
            path="%(model)s/{id}/",
            view=".views.show",
            request_method="GET",
            renderer="json"),
        "detail information about %(model)s object"
    )
    builder.define(
        i.IEdit,
        APISetCustomizer(
            route="%(model)s.unit",
            path="%(model)s/{id}/",
            view=".views.edit",
            request_method="PUT",
            renderer="json"),
        "edit %(model)s object"
    )
    builder.define(
        i.IDelete,
        APISetCustomizer(
            route="%(model)s.unit",
            path="%(model)s/{id}/",
            view=".views.delete",
            request_method="DELETE",
            renderer="json"),
        "delete %(model)s object",
        no_content=True
    )

    # children
    from sqlalchemy.orm.base import ONETOMANY, MANYTOMANY

    def has_children(customizer):
        direction = customizer.prop.direction
        return direction == ONETOMANY or direction == MANYTOMANY

    builder.define(
        i.IListing,
        IndirectAPISetCustomizer(
            route="%(model)s.%(child)s",
            path="%(model)s/{id}/%(child)s/",
            view=".views.listing_children",
            predicate=has_children,
            request_method="GET",
            renderer="json"
        ),
        "listing children of %(model)s object"
    )

    builder.define(
        i.IAddChild,
        IndirectAPISetCustomizer(
            route="%(model)s.%(child)s",
            path="%(model)s/{id}/%(child)s/",
            view=".views.create_child",
            predicate=has_children,
            request_method="POST",
            renderer="json"
        ),
        "create object as members of %(model)s's children"
    )

    builder.define(
        i.ICreateChild,
        IndirectAPISetCustomizer(
            route="%(model)s.%(child)s.unit",
            path="%(model)s/{id}/%(child)s/{child_id}/",
            view=".views.add_child",
            predicate=has_children,
            request_method="PUT",
            renderer="json"
        ),
        "take part in a members of %(model)s's children"
    )

    builder.define(
        i.IRemoveChild,
        IndirectAPISetCustomizer(
            route="%(model)s.%(child)s.unit",
            path="%(model)s/{id}/%(child)s/{child_id}/",
            view=".views.remove_child",
            predicate=has_children,
            request_method="DELETE",
            renderer="json"
        ),
        "remove from members of %(model)s's children",
        no_content=True
    )

    from sqlalchemy.orm.base import MANYTOONE

    builder.define(
        i.IListing,
        IndirectAPISetCustomizer(
            route="%(model)s.%(child)s",
            path="%(model)s/{id}/%(child)s/",
            view=".views.show_child",
            predicate=lambda customizer: customizer.prop.direction == MANYTOONE,
            request_method="GET",
            renderer="json"
        ),
        "listing %(model)s's children'"
    )


def add_apiset(config, model, name=None, **kwargs):
    builder = config.registry.getUtility(i.IAPISetBuilder)
    builder.build(model, name=name, **kwargs)


def add_custom_executor(config, scene_name, model, executor):
    builder = config.registry.getUtility(i.IAPISetBuilder)
    builder.scene_manager.add_custom_executor(scene_name, model, executor)


def add_custom_data_validation(config, scene_name, model, data_validation):
    builder = config.registry.getUtility(i.IAPISetBuilder)
    builder.scene_manager.add_custom_data_validation(scene_name, model, data_validation)


def set_dbsession(config, session):
    config.registry.registerUtility(session, i.IDBSession)


def add_model_renderer(config, Base):
    from pyramid.renderers import JSON
    renderer = JSON()
    factory = ModelRendererFactory(renderer)
    config.add_renderer("json", factory(Base))


def initialize(config, Base, session):
    config.set_komet_dbsession(session)
    config.add_komet_model_renderer(Base)


class CachedSchemaFactory(object):
    def __init__(self, schema_factory):
        self.schema_factory = schema_factory
        self.cache = {}

    def for_cache(self, x):
        if x is None:
            return None
        elif isinstance(x, (tuple, list)):
            return tuple(x)
        elif hasattr(x, "items"):
            return tuple(x.items())
        else:
            return x

    def __getattr__(self, k):
        return getattr(self.schema_factory, k)

    def __call__(self, src, includes=None, excludes=None, overrides=None, depth=None):
        k_includes = self.for_cache(includes)
        k_excludes = self.for_cache(excludes)
        k_overrides = self.for_cache(overrides)
        k_depth = self.for_cache(depth)
        k = tuple([src, k_includes, k_excludes, k_overrides, k_depth])
        try:
            return self.cache[k]
        except KeyError:
            v = self.cache[k] = self.schema_factory(src, includes=includes, excludes=excludes, overrides=overrides, depth=depth)
            return v


def includeme(config):
    config.include(define_default_apiset_builder)
    config.add_directive("add_komet_apiset", add_apiset)
    config.add_directive("set_komet_dbsession", set_dbsession)
    config.add_directive("add_komet_custom_executor", add_custom_executor)
    config.add_directive("add_komet_custom_data_validation", add_custom_data_validation)
    config.add_directive("add_komet_model_renderer", add_model_renderer)
    config.add_directive("komet_initialize", initialize)

    config.registry.registerUtility(IndexFromRequest, i.IRequestParser)
    config.registry.registerUtility(config.maybe_dotted(".repository.DefaultSQLARepository"), i.IRepository)
    config.registry.adapters.register([i.ICreate], i.IExecutor, "", config.maybe_dotted(".executors.CreateExecutor"))
    config.registry.adapters.register([i.IEdit], i.IExecutor, "", config.maybe_dotted(".executors.EditExecutor"))
    config.registry.adapters.register([i.IDelete], i.IExecutor, "", config.maybe_dotted(".executors.DeleteExecutor"))

    def dummy_data_validation(context, params, ob):
        return params

    config.registry.adapters.register([i.ICreate], i.IDataValidation, "", dummy_data_validation)
    config.registry.adapters.register([i.IEdit], i.IDataValidation, "", dummy_data_validation)
    config.registry.adapters.register([i.IDelete], i.IDataValidation, "", dummy_data_validation)

    # jsonschema
    config.registry.adapters.register([i.ICreate], i.ISchemaValidation, "", config.maybe_dotted(".executors.create_jsonschema_validation"))
    config.registry.adapters.register([i.IEdit], i.ISchemaValidation, "", config.maybe_dotted(".executors.edit_jsonschema_validation"))
    config.registry.adapters.register([i.IDelete], i.ISchemaValidation, "", config.maybe_dotted(".executors.delete_jsonschema_validation"))

    from alchemyjsonschema import SingleModelWalker, SchemaFactory
    factory = CachedSchemaFactory(SchemaFactory(SingleModelWalker))
    config.registry.registerUtility(factory, i.ISchemaFactory)
