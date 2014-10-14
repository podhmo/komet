# -*- coding:utf-8 -*-
import copy
from zope.interface import implementer
from .interfaces import (
    IExecutor,
    ISchemaValidation,
    IDataValidation,
    ICreate,
    IDelete,
    IEdit
)
from alchemyjsonschema.dictify import (
    normalize,
    validate_all,
    ErrorFound
)
from jsonschema import FormatChecker
from jsonschema.validators import Draft4Validator


class ValidationError(Exception):
    pass


@implementer(IExecutor)
class Executor(object):
    def __init__(self, context, params):
        self.context = context
        self.raw_params = params
        self.params = None

    def validation(self, ob=None):
        raise NotImplemented

    def execute(self, ob=None):
        raise NotImplemented


def default_validation(self, iface, ob=None, name=""):
    fn = self.context.customized_or_default(iface, ISchemaValidation, name=name)
    params = fn(self.context, self.raw_params)
    fn2 = self.context.customized_or_default(iface, IDataValidation, name=name)
    fn2(self.context, params, ob)
    return params


class CreateExecutor(Executor):
    def validation(self, ob=None):
        self.params = default_validation(self, ICreate, ob)

    def execute(self, ob=None):
        if self.params is None:
            raise RuntimeError("execute after validation")
        ob = self.context.modelclass(**self.params)
        self.context.session.add(ob)
        self.context.session.flush()
        return ob


class EditExecutor(Executor):
    def validation(self, ob=None):
        self.params = default_validation(self, IEdit, ob)

    def execute(self, ob):
        if self.params is None:
            raise RuntimeError("execute after validation")
        for k, v in self.params.items():
            setattr(ob, k, v)
        self.context.session.add(ob)
        return ob


class DeleteExecutor(Executor):
    def validation(self, ob=None):
        self.params = default_validation(self, IDelete, ob)

    def execute(self, ob):
        self.context.session.delete(ob)
        return ob


def create_jsonschema_validation(context, params, ob=None):
    def customize_schema(schema):
        schema = copy.deepcopy(schema)
        # when creating model, id is not needed.
        if "id" in schema["required"]:
            schema["required"].remove("id")
        if "id" in schema["properties"]:
            schema["properties"].pop("id")
        return schema

    schema = customize_schema(context.schema)
    schema_validator = Draft4Validator(schema, format_checker=FormatChecker())
    try:
        validate_all(params, schema_validator)
    except ErrorFound as err:
        raise ValidationError({e.path[0]: e.message for e in err.errors})
    return normalize(params, schema)


def edit_jsonschema_validation(context, params):
    schema = context.schema
    schema_validator = Draft4Validator(schema, format_checker=FormatChecker())
    try:
        validate_all(params, schema_validator)
    except ErrorFound as err:
        raise ValidationError({e.path[0]: e.message for e in err.errors})
    return normalize(params, schema)


def delete_jsonschema_validation(context, params):
    return params
