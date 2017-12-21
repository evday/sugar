#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2017-12-21,16:28"

from django.template import Library
from django.urls import reverse

from stark.service.star import site

register = Library()

@register.inclusion_tag("stark/form.html")
def form(model_form_obj):
    '''
    自定义标签，处理popup
    :param model_form_obj:
    :return:
    '''
    new_form = []
    for bfield in model_form_obj:  #这里的
        temp = {"is_popup":False,"item":bfield}
        from django.forms.models import ModelChoiceField
        if isinstance(bfield.field,ModelChoiceField):
            related_class_name = bfield.field.queryset.model  #根据字段找多啊表名
            if related_class_name in site._registry: #说明是注册到stark.py 中的
                app_model_name = related_class_name._meta.app_label,related_class_name._meta.model_name
                base_url = reverse("stark:%s_%s_add"%app_model_name) #拼接页面路径
                popurl = "%s?_popbackid=%s"%(base_url,bfield.auto_id)
                temp["is_popup"] = True
                temp["popup_url"] = popurl
        new_form.append(temp)
    return {"form":new_form}



