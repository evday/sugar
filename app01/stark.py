#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2017-12-14,14:51"
from stark.service import star
from . import models




star.site.register(models.UserInfo)
star.site.register(models.Role)