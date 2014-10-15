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


def listing_children(context, request):
    repository = context.repository
    ob = repository[context.get_index()]
    if ob is None:
        raise APINotFound("")
    return list(getattr(ob, context.prop.key))


def show_child(context, request):
    repository = context.repository
    ob = repository[context.get_index()]
    if ob is None:
        raise APINotFound("")
    return getattr(ob, context.prop.key)


def schema(context, request):
    return context.schema


def show(context, request):
    repository = context.repository
    ob = repository[context.get_index()]
    if ob is None:
        raise APINotFound("")
    return ob


def edit(context, request):
    repository = context.repository
    ob = repository[context.get_index()]
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
    ob = repository[context.get_index()]
    if ob is None:
        raise APINotFound("")
    executor = context.get_executor(IDelete)
    try:
        executor.validation(ob=ob)
    except ValidationError as e:
        raise context.httpexception(e)
    ob = executor.execute(ob=ob)
    return ob  # dummy?
