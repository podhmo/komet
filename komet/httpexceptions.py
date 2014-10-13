# -*- coding:utf-8 -*-
from pyramid import httpexceptions as exc
from pyramid.response import Response
import json


class APIError(exc.HTTPError):
    code = 400
    msg = "APIError"

    def __init__(self, msg=None):
        body = {'status': self.code, 'message': msg or self.msg}
        Response.__init__(self, json.dumps(body))
        self.status = self.code
        self.content_type = 'application/json'


class APIBadRequest(APIError):
    pass


class APIUnauthorized(APIError):
    code = 401
    msg = "Unauthorized"


class APINotFound(APIError):
    code = 404
    msg = "Not found"
