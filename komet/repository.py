# -*- coding:utf-8 -*-
from pyramid.decorator import reify
import sqlalchemy as sa
from zope.interface import implementer
from .interfaces import (
    IRepository
)


@implementer(IRepository)
class DefaultSQLARepository(object):
    def __init__(self, request, model, session):
        self.request = request
        self.model = model
        self.session = session

    def __getitem__(self, i):
        return self.query.get(i)

    def _get_maybe_int(self, k, default):
        try:
            return int(self.request.GET.get(k, default))
        except (ValueError, TypeError):
            return default

    @reify
    def query(self):  # xxx:
        q = self.session.query(self.model)
        sort_key = self.request.GET.get("sort")
        if sort_key:
            direction = self.request.GET.get("direction", "asc")
            direction = sa.desc if direction == "desc" else sa.asc
            q = q.order_by(direction(sort_key))

        page = self._get_maybe_int("page", None)
        limit = self._get_maybe_int("limit", 10)

        if page:
            q = q.offset(limit * page)
        if limit:
            q = q.limit(limit)
        return q

    def __iter__(self):
        for x in self.query.all():
            yield x
