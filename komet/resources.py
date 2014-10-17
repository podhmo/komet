# -*- coding:utf-8 -*-
import copy
from pyramid.decorator import reify
from zope.interface import implementer, implementedBy
from .httpexceptions import APIBadRequest
from . import interfaces as i


@implementer(i.IModelResource)
class KometResource(object):
    def __init__(self, request, modelclass):
        self.request = request
        self.modelclass = modelclass

    def get_another_resource(self, modelclass):
        return self.__class__(self.request, modelclass)

    @reify
    def adapter(self):
        return self.request.registry.adapters.lookup

    @reify
    def utility(self):
        return self.request.registry.getUtility

    @reify
    def session(self):
        return self.utility(i.IDBSession)

    @reify
    def repository(self):
        return self.utility(i.IRepository)(self.request, self.modelclass, self.session)

    @reify
    def schema(self):
        return self.utility(i.ISchemaFactory)(self.modelclass)

    @reify
    def schema_information(self):
        link_manager = self.adapter((implementedBy(self.modelclass), ), i.IModelLinkManager) or []
        schema = copy.copy(self.schema)
        links = []
        for link in link_manager:
            links.append(link)
        schema["links"] = links
        return schema

    @reify
    def parser(self):
        return self.utility(i.IRequestParser)(self.request)

    def customized_or_default(self, src, dst, name=""):
        fn = self.adapter((implementedBy(self.modelclass), src), dst, name=name)
        if fn is None:
            fn = self.adapter((src, ), dst, name=name)
            if fn is None:
                raise RuntimeError("%s -> %s is not found.", src, dst)
            # cache
            self.request.registry.registerAdapter(fn, (self.modelclass, src), dst, event=False, name=name)
        return fn

    def get_executor(self, scene, name=""):
        fn = self.customized_or_default(scene, i.IExecutor)
        return fn(self, self.request.json_body)

    def httpexception(self, err):
        return APIBadRequest(err.args[0])  # xxx


def resource_factory(modelclass):
    return lambda request: KometResource(request, modelclass)
