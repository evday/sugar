#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2017-12-14,14:51"
from stark.service import star
from . import models
from stark.service import star


class UserInfoConfig(star.StarkConfig):
    list_display = ["id","name"]

star.site.register(models.UserInfo,UserInfoConfig)
star.site.register(models.Role)