# -*- coding:utf-8 -*-
from sqlash import SerializerFactory
import sqlalchemy.types as t
from functools import wraps
from .builder import ModelLink


def maybe_none(fn):
    @wraps(fn)
    def wrapper(v, r):
        if v is None:
            return None
        return fn(v, r)
    return wrapper


@maybe_none
def datetime_for_human(dt, r):
    return dt.strftime("%Y/%m/%dT%H:%M:%S.%f%z")

default_convertions = {
    t.DateTime: datetime_for_human
}


class ModelRendererFactory(object):
    def __init__(self, renderer, convertions=default_convertions):
        self.renderer = renderer
        self.serializer = SerializerFactory(convertions=convertions)()

    def jsonify_sqlaobject(self, ob, request):
        result = self.serializer.serialize(ob, [":ALL:"])
        result["type"] = ob.__class__.__name__
        return result

    def jsonify_model_link(self, ob, request):
        result = {
            "title": ob.title,
            "method": ob.method,
            "href": ob.href,
            "rel": ob.rel,
        }
        if not ob.no_content:
            result["mediaType"] = "application/json"  # request
            result["encType"] = "application/json"  # response
        return result

    def __call__(self, Base):
        self.renderer.add_adapter(Base, self.jsonify_sqlaobject)
        self.renderer.add_adapter(ModelLink, self.jsonify_model_link)
        return self.renderer
