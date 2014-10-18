# -*- coding:utf-8 -*-
def allow_cross_origin_tween(handler, registry):
    def _wrapper(request):
        response = handler(request)
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response
    return _wrapper
