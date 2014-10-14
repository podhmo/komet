# -*- coding:utf-8 -*-
import logging
logging.basicConfig(level=logging.DEBUG)

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

DBSession = orm.scoped_session(orm.sessionmaker())
Base = declarative_base()


class Point(Base):
    __tablename__ = "points"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)
    value = sa.Column(sa.Integer, nullable=False)
    created_at = sa.Column(sa.DateTime(), nullable=False, default=datetime.now)


def setup_module(module):
    engine = sa.create_engine('sqlite:///:memory:', echo=False)
    DBSession.bind = engine
    Base.metadata.bind = engine
    Base.metadata.create_all()


def make_config(settings):
    from pyramid.config import Configurator
    config = Configurator(settings=settings)

    config.include("komet")
    config.komet_initialize(Base, DBSession)
    config.add_komet_apiset(Point, "point")
    return config


def make_app(config):
    app = config.make_wsgi_app()
    return app


def test_it():
    from komet.testing import TestRESTApp
    config = make_config({"debug_notfound": True, "debug_routematch": True})
    app = TestRESTApp(make_app(config))

    # listing model
    response = app.get_json("/points/")
    assert response.status_code == 200
    assert len(response.json_body) == 0

    # create model
    params = {"name": "normal", "value": 100}
    response = app.post_json("/points/", params)
    assert response.status_code == 200

    # listing model (after crerate model)
    response = app.get_json("/points/")
    assert response.status_code == 200
    assert len(response.json_body) == 1

    # edit model
    id = response.json_body[0]["id"]
    params = {"id": id, "name": "updated", "value": 100}
    response = app.put_json("/points/{}/".format(id), params)
    assert response.status_code == 200
    assert response.json_body["name"] == "updated"

    # delete model
    response = app.delete_json("/points/{}/".format(id))
    assert response.status_code == 200

    # listing model (after delete model)
    response = app.get_json("/points/")
    assert response.status_code == 200
    assert len(response.json_body) == 0
