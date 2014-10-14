# -*- coding:utf-8 -*-
def _getTarget():
    from komet.builder import IndirectAPISetCustomizer
    return IndirectAPISetCustomizer

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255), default="", nullable=False)
    group_id = sa.Column(sa.Integer, sa.ForeignKey("groups.id"))
    group = orm.relationship("Group", backref="users", uselist=False)


class Group(Base):
    __tablename__ = "groups"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255), default="", nullable=False)


def test_detect_relationship_from_model__one_to_many():
    route = object()
    path = object()
    view = object()
    predicate = object()

    target = _getTarget()(route, path, view, predicate)

    result = list(target.detect_relationships(Group))
    assert len(result) == 1
    assert result[0].key == "users"


def test_detect_relationship_from_model__many_to_one():
    route = object()
    path = object()
    view = object()
    predicate = object()

    target = _getTarget()(route, path, view, predicate)

    result = list(target.detect_relationships(User))
    assert len(result) == 1
    assert result[0].key == "group"


def test_iterate_only_many_to_one_predicate__found():
    route = object()
    path = object()
    view = object()

    def predicate(customizer):
        from sqlalchemy.orm.base import MANYTOONE
        return customizer.prop.direction == MANYTOONE

    target = _getTarget()(route, path, view, predicate)

    result = list(target.iterate(User))
    assert len(result) == 1


def test_iterate_only_many_to_one_predicate__not_found():
    route = object()
    path = object()
    view = object()

    def predicate(customizer):
        from sqlalchemy.orm.base import MANYTOONE
        return customizer.prop.direction == MANYTOONE

    target = _getTarget()(route, path, view, predicate)

    result = list(target.iterate(Group))
    assert len(result) == 0
