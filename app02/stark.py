#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date:"2017-12-14,14:51"
from django.forms import ModelForm
from django.conf.urls import url
from django.shortcuts import HttpResponse, redirect, render
from django.utils.safestring import mark_safe
from django.urls import reverse

from stark.service import star
from . import models


class HostConfigForm(ModelForm):
    class Meta:
        model = models.Host
        fields = "__all__"
        error_messages = {
            "hostname": {"required": "主机名不能为空"},
            "ip": {
                "required": "IP不能为空",
                "invalid": "IP格式错误"
            },
            "port": {
                "required": "端口不能为空",
            }
        }


class HostConfig(star.StarkConfig):
    #自定制列
    def is_port(self, obj=None, is_header=False):
        if is_header:
            return "报表"
        return mark_safe("<a href='%s'><button class='btn btn-info'>报表</button></a>"%(obj.id))

    # 显示列
    list_display = ["id", "hostname", "ip", "port",is_port]

    # Booklist = []
    # for i in range(200):
    #     Booklist.append(models.Host(hostname='eccgw01.boulder.ibm.com',ip='129.42.160.51',port=443))
    # models.Host.objects.bulk_create(Booklist)
    # 是否显示增加按钮
    show_add_btn = True
    # 自定义错误信息
    model_form_class = HostConfigForm

    # 扩展url
    def extra_url(self):

        urlpatterns = [
            url(r'^report/$', self.report_view)
        ]
        return urlpatterns

    def report_view(self, request):
        return HttpResponse("自定义报表")

    # 自定义删除视图
    def delete_view(self, request, nid, *args, **kwargs):
        if request.method == "GET":
            return render(request, 'my_delete.html', {"back_url": self.get_changelist_url()})
        else:
            self.model_class.objects.filter(pk=nid).delete()
            return redirect(self.get_changelist_url())

star.site.register(models.Host, HostConfig)
