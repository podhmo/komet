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
                            config.maybe_dotted(".models.DBSession"))
    config.add_komet_apiset(config.maybe_dotted(".models.MyModel"), "mymodel")

    ## ui
    config.add_mako_renderer(".html")
    config.add_static_view("bower", '../bower_components')

    config.scan()
    return config.make_wsgi_app()
