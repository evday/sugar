#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2017-12-14,15:03"

class StarkConfig(object):
    pass


class StarkSite(object):
    def __init__(self):
        self._registry = {}


    def register(self,model_class,stark_config_obj = None):
        if not stark_config_obj:
            stark_config_obj = StarkConfig

        self._registry[model_class] = stark_config_obj(model_class,self)




