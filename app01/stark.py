#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2017-12-14,14:51"
from stark.service import star
from . import models
from stark.service import star
from django.utils.safestring import mark_safe


class UserInfoConfig(star.StarkConfig):

    def checkbox(self,obj = None,is_header = False):
        if is_header:
            return '选择'
        return mark_safe("<input type='checkbox' name='pk' val= %s>"%(obj.id,))

    def edit(self,obj = None,is_header = False):
        if is_header:
            return "编辑"
        return mark_safe("<a href='/edit/%s'>编辑</a>"%(obj.id,))

    list_display = [checkbox,"id","name",edit]


star.site.register(models.UserInfo,UserInfoConfig)
star.site.register(models.Role)