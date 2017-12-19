#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2017-12-14,14:51"
from stark.service import star
from django.conf.urls import url
from django.forms import ModelForm
from . import models
from stark.service import star

from django.shortcuts import HttpResponse



class UserInfoForm(ModelForm):
    class Meta:
        model = models.UserInfo
        fields = "__all__"
        error_messages = {
            "name":{"required":"用户名不能为空"},
            "pwd":{"required":"密码不能为空"},
            "emil":{
                'required': '邮箱不能为空',
                'invalid': '邮箱格式错误',
            }
        }

class UserInfoConfig(star.StarkConfig):


    show_add_btn = True

    model_form_class = UserInfoForm

    list_display = ["id","name","emil"] #先找自己的list_display

    search_fields = ["name__contains",'emil__contains'] #__contains 模糊搜索

    show_search_form = True

    show_actions = True

    def multi_del(self,request):

        print(request.POST)
        pk_list = request.POST.getlist("pk") #这个pk是我们在checkbook方法设置的

        self.model_class.objects.filter(id__in = pk_list).delete()
    multi_del.short_desc = "批量删除"

    actions = [multi_del,]


star.site.register(models.UserInfo,UserInfoConfig)


class RoleConfig(star.StarkConfig):
    list_display = ["id", "caption"]
star.site.register(models.Role,RoleConfig)