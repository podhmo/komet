# -*- coding:utf-8 -*-
from .executors import ValidationError
from .httpexceptions import APINotFound
from .interfaces import (
    ICreate,
    IEdit,
    IDelete
)


def create(context, request):
    executor = context.get_executor(ICreate)
    try:
        executor.validation(ob=None)
    except ValidationError as e:
        raise context.httpexception(e)
    ob = executor.execute()
    return ob


def listing(context, request):
    repository = context.repository
    obs = list(repository)
    return obs


def listing_children(context, request):  # xxx:
    repository = context.repository
    ob = repository[context.parser.get_index()]
    if ob is None:
        raise APINotFound("")
    return list(getattr(ob, context.prop.key))


def create_child(context, request):  # xxx:
    repository = context.repository
    ob = repository[context.parser.get_index()]
    if ob is None:
        raise APINotFound("")
    another = context.get_another_resource(context.prop.mapper.class_)

    executor = another.get_executor(ICreate)
    try:
        executor.validation(ob=None)
    except ValidationError as e:
        raise another.httpexception(e)
    child = executor.execute()
    getattr(ob, context.prop.key).append(child)
    return {"parent": ob, "child": child}


def add_child(context, request):  # xxx:
    repository = context.repository
    ob = repository[context.parser.get_index()]
    if ob is None:
        raise APINotFound("")
    another = context.get_another_resource(context.prop.mapper.class_)
    child = another.repository[context.parser.get_child_index()]
    if child is None:
        raise APINotFound("")
    getattr(ob, context.prop.key).append(child)
    return {"parent": ob, "child": child}


def remove_child(context, request):  # xxx:
    repository = context.repository
    ob = repository[context.parser.get_index()]
    if ob is None:
        raise APINotFound("")
    another = context.get_another_resource(context.prop.mapper.class_)
    child = another.repository[context.parser.get_child_index()]
    if child is None:
        raise APINotFound("")
    getattr(ob, context.prop.key).remove(child)
    return {"parent": ob, "child": child}


def show_child(context, request):  # xxx:
    repository = context.repository
    ob = repository[context.parser.get_index()]
    if ob is None:
        raise APINotFound("")
    return getattr(ob, context.prop.key)


def schema(context, request):
    return context.schema_information


def show(context, request):
    repository = context.repository
    ob = repository[context.parser.get_index()]
    if ob is None:
        raise APINotFound("")
    return ob


def edit(context, request):
    repository = context.repository
    ob = repository[context.parser.get_index()]
    if ob is None:
        raise APINotFound("")
    executor = context.get_executor(IEdit)
    try:
        executor.validation(ob=ob)
    except ValidationError as e:
        raise context.httpexception(e)
    ob = executor.execute(ob=ob)
    return ob


def delete(context, request):
    repository = context.repository
    ob = repository[context.parser.get_index()]
    if ob is None:
        raise APINotFound("")
    executor = context.get_executor(IDelete)
    try:
        executor.validation(ob=ob)
    except ValidationError as e:
        raise context.httpexception(e)
    ob = executor.execute(ob=ob)
    return ob  # dummy?
