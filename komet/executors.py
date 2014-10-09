# -*- coding:utf-8 -*-
from zope.interface import implementer

from .interfaces import (
    IExecutor
)


class ValidationError(Exception):
    def __init__(self, params, errors, ob=None):
        self.initials = params
        self.errors = errors
        self.ob = ob

    def as_dict(self):
        return self.errors


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
        self.params = self.raw_params
        # raise ValidationError()

    def execute(self, ob=None):
        if self.params is None:
            raise RuntimeError("execute after validation")
        ob = self.context.modelclass(**self.params)
        self.context.session.add(ob)
        return ob


class EditExecutor(Executor):
    def validation(self):
        self.params = self.raw_params
        # raise ValidationError()

    def execute(self, ob):
        if self.params is None:
            raise RuntimeError("execute after validation")
        for k, v in self.params.items():
            setattr(ob, k, v)
        self.context.session.add(ob)
        return ob


class DeleteExecutor(Executor):
    def validation(self):
        self.params = self.raw_params
        # raise ValidationError()

    def execute(self, ob):
        if self.params is None:
            raise RuntimeError("execute after validation")
        self.context.session.delete(ob)
        return ob
