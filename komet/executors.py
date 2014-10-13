# -*- coding:utf-8 -*-
import copy
from zope.interface import implementer
from .interfaces import (
    IExecutor,
    IValidation,
    ICreate,
    IDelete,
    IEdit
)
from alchemyjsonschema.dictify import (
    normalize,
    validate_all
)
from jsonschema import FormatChecker
from jsonschema.validators import Draft4Validator


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


class CreateExecutor(Executor):
    def validation(self, ob=None):
        fn = self.context.customized_or_default([ICreate], IValidation)
        self.params = fn(self.context, self.raw_params, ob)

    def execute(self, ob=None):
        if self.params is None:
            raise RuntimeError("execute after validation")
        ob = self.context.modelclass(**self.params)
        self.context.session.add(ob)
        self.context.session.flush()
        return ob


class EditExecutor(Executor):
    def validation(self, ob):
        fn = self.context.customized_or_default([IEdit], IValidation)
        self.params = fn(self.context, self.raw_params, ob)

    def execute(self, ob):
        if self.params is None:
            raise RuntimeError("execute after validation")
        for k, v in self.params.items():
            setattr(ob, k, v)
        self.context.session.add(ob)
        return ob


class DeleteExecutor(Executor):
    def validation(self, ob):
        fn = self.context.customized_or_default([IDelete], IValidation)
        self.params = fn(self.context, self.raw_params, ob)

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
    validate_all(params, schema_validator)
    return normalize(params, schema)


def edit_jsonschema_validation(context, params, ob):
    schema = context.schema
    schema_validator = Draft4Validator(schema, format_checker=FormatChecker())
    validate_all(params, schema_validator)
    return normalize(params, schema)


def delete_jsonschema_validation(context, params, ob):
    return params
