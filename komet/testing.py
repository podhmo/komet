# -*- coding:utf-8 -*-
class TestRESTApp(object):
    """tiny webtest like testing middleware"""
    def __init__(self, app):
        self.app = app

    def post_json(self, path, params=None):
        request = self._make_request("POST", path, params)
        return self.app.invoke_subrequest(request, use_tweens=True)

    def get_json(self, path, params=None):
        request = self._make_request("GET", path, params)
        return self.app.invoke_subrequest(request, use_tweens=True)

    def put_json(self, path, params=None):
        request = self._make_request("PUT", path, params)
        return self.app.invoke_subrequest(request, use_tweens=True)

    def delete_json(self, path, params=None):
        request = self._make_request("DELETE", path, params)
        return self.app.invoke_subrequest(request, use_tweens=True)

    def _make_request(self, method, path, params):
        from pyramid.testing import DummyRequest

        if not path.endswith("/"):
            path = path + "/"

        return DummyRequest(
            path=path,
            registry=self.app.registry,
            content_type="application/json",
            method=method,
            environ={"PATH_INFO": path},
            json_body=params or {})

