#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2017-12-14,14:51"
from stark.service import star
from django.conf.urls import url
from . import models
from stark.service import star

from django.shortcuts import HttpResponse


class UserInfoConfig(star.StarkConfig):


    #
    # def extra_url(self):
    #     urlpatterns = [
    #         url(r'^xxxx/$',self.func)
    #     ]
    #     return urlpatterns
    #
    # def func(self,request):
    #     return HttpResponse("hello")

    list_display = ["id","name"] #先找自己的list_display


star.site.register(models.UserInfo,UserInfoConfig)


class RoleConfig(star.StarkConfig):
    list_display = ["id", "caption"]
star.site.register(models.Role,RoleConfig)