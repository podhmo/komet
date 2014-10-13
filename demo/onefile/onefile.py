import logging
logger = logging.getLogger(__name__)

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
import os.path


## model
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime

Session = scoped_session(sessionmaker())
engine = sa.create_engine('sqlite:///onefile.db', echo=True)
Session.configure(bind=engine)

Base = declarative_base(bind=engine)


class User(Base):
    __tablename__ = "User"
    query = Session.query_property()

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255), default="", nullable=False, unique=True)
    description = sa.Column(sa.String(255), default="", nullable=False)
    age = sa.Column(sa.Integer)
    created_at = sa.Column(sa.DateTime, default=datetime.now, nullable=False)


def top_view(request):
    return {}


def simple_commit_tween(handler, registry):  # todo:fix
    from komet.httpexceptions import APIBadRequest

    def tween(request):
        try:
            response = handler(request)
            if hasattr(request.context, "session"):
                request.context.session.commit()
        except Exception as e:
            logger.exception(e)
            if hasattr(request.context, "session"):
                request.context.session.rollback()
            return APIBadRequest(repr(e))
        return response
    return tween


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    settings = {"mako.directories": here,
                "pyramid.reload_all": True}

    Base.metadata.drop_all()
    Base.metadata.create_all()

    Session.add(User(name="foo", age=20))
    Session.commit()

    config = Configurator(settings=settings)
    config.include("pyramid_mako")

    config.add_tween("onefile.simple_commit_tween")

    ## komet::
    config.include("komet")
    config.add_komet_dbsession(Session)
    config.add_komet_model_renderer(Base)
    config.add_komet_apiset(User, "user")


    ## ui::
    config.add_mako_renderer(".html")
    config.add_route('top', '/')
    config.add_view(top_view, route_name='top', renderer="onefile.html")
    config.add_static_view("static", path="%(here)s/static" % {"here": here})
    config.add_static_view("bower", path="%(here)s/bower_components" % {"here": here})

    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 7654, app)
    server.serve_forever()
