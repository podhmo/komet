# -*- coding:utf-8 -*-
from zope.interface import Interface, Attribute


class IDBSession(Interface):
    def add(ob):
        pass

    def delete(ob):
        pass


class IAPISetBuilder(Interface):
    def define(route, scene, path, view, **kwargs):
        pass

    def build(model, name=None, **kwargs):
        pass


class IModelResource(Interface):
    request = Attribute("")
    modelclass = Attribute("")
    repository = Attribute("")
    session = Attribute("")

    def get_executor(scene):
        pass

    def get_index():
        pass

    def httpexception(err):
        pass


class IRepository(Interface):
    def __getitem__(k):
        pass

    def __iter__():
        pass


class ISchemaFactory(Interface):
    def __call__(modelclass):
        pass


class IExecutor(Interface):
    def validation(ob=None):
        pass

    def execute(ob=None):
        pass


class ISchemaValidation(Interface):
    def __call__(context, params):
        pass


class IDataValidation(Interface):
    def __call__(context, params, ob=None):
        pass


class IIndexFromRequest(Interface):
    def __call__(request):
        """get index from request (usually from request.matchdict)"""


class IScene(Interface):
    pass


class IListing(IScene):
    pass


class ICreate(IScene):
    pass


class IEdit(IScene):
    pass


class IDelete(IScene):
    pass


class IShow(IScene):
    pass

