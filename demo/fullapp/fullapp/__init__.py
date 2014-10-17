from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_mako')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('foo', '/foo')
    config.add_route('boo', '/boo')

    config.include("komet")
    config.komet_initialize(config.maybe_dotted(".models.Base"),
                            config.maybe_dotted(".models.DBSession"),
                        )

    def add_apiset(model, name):
        config.add_komet_apiset(model, name, prefix="/api")

    add_apiset(config.maybe_dotted(".models.MyModel"), "mymodels")

    # one to many
    add_apiset(config.maybe_dotted(".models.User"), "users")
    add_apiset(config.maybe_dotted(".models.Group"), "groups")

    # many to many
    add_apiset(config.maybe_dotted(".models.Member"), "members")
    add_apiset(config.maybe_dotted(".models.Team"), "teams")

    # complex (from colanderalchemy)
    add_apiset(config.maybe_dotted(".models.Account"), "accounts")
    add_apiset(config.maybe_dotted(".models.Person"), "people")
    add_apiset(config.maybe_dotted(".models.PersonGroup"), "pgroups")
    add_apiset(config.maybe_dotted(".models.Address"), "addresses")

    # ui
    config.add_mako_renderer(".html")
    config.add_static_view("bower", '../bower_components')

    config.scan()
    return config.make_wsgi_app()
