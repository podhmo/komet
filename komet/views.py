# -*- coding:utf-8 -*-
from alchemyjsonschema.dictify import ErrorFound
from pyramid.httpexceptions import HTTPNotFound
from .interfaces import (
    ICreate,
    IEdit,
    IDelete
)


def create(context, request):
    executor = context.get_executor(ICreate)
    try:
        executor.validation(ob=None)
    except ErrorFound as e:
        raise context.httpexception(e)
    ob = executor.execute()
    return ob


def listing(context, request):
    repository = context.repository
    obs = list(repository)
    return obs


def schema(context, request):
    return context.schema


def show(context, request):
    repository = context.repository
    ob = repository[context.get_index()]
    if ob is None:
        raise HTTPNotFound("")
    return ob


def edit(context, request):
    repository = context.repository
    ob = repository[context.get_index()]
    if ob is None:
        raise HTTPNotFound("")
    executor = context.get_executor(IEdit)
    try:
        executor.validation(ob=ob)
    except ErrorFound as e:
        raise context.httpexception(e)
    ob = executor.execute(ob=ob)
    return ob


def delete(context, request):
    repository = context.repository
    ob = repository[context.get_index()]
    if ob is None:
        raise HTTPNotFound("")
    executor = context.get_executor(IDelete)
    try:
        executor.validation(ob=ob)
    except ErrorFound as e:
        raise context.httpexception(e)
    ob = executor.execute(ob=ob)
    return ob  # dummy?
