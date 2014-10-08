from wsgiref.simple_server import make_server
from pyramid.config import Configurator
import os.path


## model
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import scoped_session, sessionmaker

Session = scoped_session(sessionmaker())
engine = sa.create_engine('sqlite:///onefile.db', echo=True)
Session.configure(bind=engine)

Base = declarative_base(bind=engine)


class User(Base):
    __tablename__ = "User"
    query = Session.query_property()

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255), default="", nullable=False)
    description = sa.Column(sa.String(255), default="", nullable=False)
    age = sa.Column(sa.Integer)


def top_view(request):
    return {}


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    settings = {"mako.directories": here,
                "pyramid.reload_all": True}

    Base.metadata.create_all()

    config = Configurator(settings=settings)
    config.include("pyramid_mako")

    ## komet::
    config.include("komet")
    config.add_komet_dbsession(Session)
    config.add_komet_apiset(User, "user")


    config.add_mako_renderer(".html")
    config.add_route('top', '/')
    config.add_view(top_view, route_name='top', renderer="onefile.html")

    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 7654, app)
    server.serve_forever()
