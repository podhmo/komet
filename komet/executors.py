# -*- coding:utf-8 -*-
import copy
from zope.interface import implementer
from .interfaces import (
    IExecutor
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
    def customize_schema(self, schema):
        schema = copy.deepcopy(schema)
        # when creating model, id is not needed.
        if "id" in schema["required"]:
            schema["required"].remove("id")
        if "id" in schema["properties"]:
            schema["properties"].pop("id")
        return schema

    def validation(self, ob=None):
        schema = self.customize_schema(self.context.schema)
        schema_validator = Draft4Validator(schema, format_checker=FormatChecker())
        validate_all(self.raw_params, schema_validator)
        self.params = normalize(self.raw_params, schema)

    def execute(self, ob=None):
        if self.params is None:
            raise RuntimeError("execute after validation")
        ob = self.context.modelclass(**self.params)
        self.context.session.add(ob)
        self.context.session.flush()
        return ob


class EditExecutor(Executor):
    def customize_schema(self, schema):
        return schema

    def validation(self, ob):
        schema = self.customize_schema(self.context.schema)
        schema_validator = Draft4Validator(schema, format_checker=FormatChecker())
        validate_all(self.raw_params, schema_validator)
        self.params = normalize(self.raw_params, schema)

    def execute(self, ob):
        if self.params is None:
            raise RuntimeError("execute after validation")
        for k, v in self.params.items():
            setattr(ob, k, v)
        self.context.session.add(ob)
        return ob


class DeleteExecutor(Executor):
    def validation(self, ob):
        self.params = self.raw_params

    def execute(self, ob):
        self.context.session.delete(ob)
        return ob
