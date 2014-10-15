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

    def parser():
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


class IRequestParser(Interface):
    def get_index():
        """get index from request (usually from request.matchdict)"""

    def get_child_index():
        """get index from request (usually from request.matchdict)"""


class IScene(Interface):
    pass


class IListing(IScene):
    name = Attribute("list")


class ICreate(IScene):
    name = Attribute("create")


class IEdit(IScene):
    name = Attribute("edit")


class IDelete(IScene):
    name = Attribute("delete")


class IShow(IScene):
    name = Attribute("show")


class IAddChild(IScene):
    name = Attribute("add_child")


class IRemoveChild(IScene):
    name = Attribute("remove_child")


class ISceneManager(Interface):
    pass


class IName(Interface):  # xxx:
    pass
