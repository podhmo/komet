# -*- coding:utf-8 -*-
from sqlash import SerializerFactory
import sqlalchemy.types as t


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
        return self.serializer.serialize(ob, [":ALL:"])

    def __call__(self, Base):
        self.renderer.add_adapter(Base, self.jsonify)
        return self.renderer
