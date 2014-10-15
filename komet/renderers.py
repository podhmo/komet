# -*- coding:utf-8 -*-
from sqlash import SerializerFactory
import sqlalchemy.types as t
from zope.interface import providedBy
from .interfaces import IName


def datetime_for_human(dt, r):
    return dt.strftime("%Y/%m/%dT%H:%M:%S.%f%z")

default_convertions = {
    t.DateTime: datetime_for_human
}


class ModelRendererFactory(object):
    def __init__(self, renderer, convertions=default_convertions):
        self.renderer = renderer
        self.serializer = SerializerFactory(convertions=convertions)()

    def jsonify(self, ob, request):
        result = self.serializer.serialize(ob, [":ALL:"])
        result["type"] = ob.__class__.__name__
        # result["resource"] = request.registry.adapters.lookup((providedBy(ob), ), IName)
        return result

    def __call__(self, Base):
        self.renderer.add_adapter(Base, self.jsonify)
        return self.renderer
