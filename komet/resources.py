# -*- coding:utf-8 -*-
from pyramid.decorator import reify
from .httpexceptions import APIBadRequest
from zope.interface import implementer
from . import interfaces as i


@implementer(i.IModelResource)
class KometResource(object):
    def __init__(self, request, modelclass):
        self.request = request
        self.modelclass = modelclass

    @reify
    def adapter(self):
        return self.request.registry.adapters.lookup

    @reify
    def utility(self):
        return self.request.registry.getUtility

    @reify
    def name(self):
        return self.modelclass.__name__

    @reify
    def session(self):
        return self.utility(i.IDBSession)

    @reify
    def repository(self):
        return self.utility(i.IRepository)(self.request, self.modelclass, self.session)

    @reify
    def schema(self):
        return self.utility(i.ISchemaFactory)(self.modelclass)

    def get_index(self):
        return self.utility(i.IIndexFromRequest)(self.request)

    def customized_or_default(self, src, dst):
        fn = self.adapter(src, dst, name=self.name)
        if fn is None:
            fn = self.adapter(src, dst, name="")
            if fn is None:
                raise RuntimeError("%s -> %s is not found.", src, dst)
            # cache
            self.request.registry.adapters.register(src, dst, self.name, fn)
        return fn

    def get_executor(self, scene):
        fn = self.customized_or_default([scene], i.IExecutor)
        return fn(self, self.request.json_body)

    def httpexception(self, err):
        return APIBadRequest(err)  # xxx


def resource_factory(modelclass):
    return lambda request: KometResource(request, modelclass)
