# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)
import venusian
from .executors import ValidationError


def custom_data_validation(scene_name, model):
    def _wrapped(data_validation):
        def callback(context, name, ob):
            config = context.config.with_package(info.module)
            config.add_komet_custom_data_validation(scene_name, model, data_validation)
        info = venusian.attach(data_validation, callback, category='pyramid')  # xxx:
        return data_validation
    return _wrapped


def includeme(config):
    config.include(".defaultconfigration")
