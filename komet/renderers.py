# -*- coding:utf-8 -*-
from alchemyjsonschema.dictify import jsonify


class ModelRendererFactory(object):
    def __init__(self, renderer):
        self.renderer = renderer

    def jsonify(self, ob, request):
        schema = request.context.schema
        return jsonify(ob, schema)

    def __call__(self, Base):
        self.renderer.add_adapter(Base, self.jsonify)
        return self.renderer
