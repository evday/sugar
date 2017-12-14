#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2017-12-14,15:03"
from django.conf.urls import url
from django.shortcuts import HttpResponse,render



class StarkConfig(object):


    list_display = []

    def __init__(self,model_class,site):
        self.model_class = model_class
        self.site = site

    def get_urls(self):

        app_model_name = (self.model_class._meta.app_label,self.model_class._meta.model_name)
        urlpatterns = [
            url(r'^$',self.classList_view,name="%s_%s_classList" %app_model_name),
            url(r'^add/$',self.add_view,name="%s_%s_add" %app_model_name),
            url(r'^(\d+)/delete/$',self.delete_view,name="%s_%s_delete" %app_model_name),
            url(r'^(\d+)/change/$',self.change_view,name="%s_%s_change" %app_model_name),
        ]
        return urlpatterns





    @property
    def urls(self):
        return self.get_urls()


    def classList_view(self,request,*args,**kwargs):
        #展示表头
        head_list = []
        for field_name in self.list_display:
            if isinstance(field_name,str):
                #根据类和字段名称获取字段对象的verbose_name

                #如果是字段的话，就获取字段的verbose_name
                verbose_name = self.model_class._meta.get_field(field_name).verbose_name
            else:
                #如果是函数的，就执行函数里面的方法
                verbose_name = field_name(self,is_header = True) #函数名加括号，调用
            head_list.append(verbose_name)

        #两层列表展示数据

        data_list = self.model_class.objects.all()

        new_data_list = []
        for row in data_list:
            temp = []
            for field_name in self.list_display:
                if isinstance(field_name,str): #不是字符串不能用getattr
                    val = getattr(row,field_name)#利用反射来查找
                else:
                    val = field_name(self,row)
                temp.append(val)
            new_data_list.append(temp)



        return render(request,"stark/classList.html",{"new_data_list":new_data_list,"head_list":head_list})

    def add_view(self,request,*args,**kwargs):
        return HttpResponse("增加")

    def delete_view(self, request,nid, *args, **kwargs):
        return HttpResponse("删除")

    def change_view(self, request, nid,*args, **kwargs):
        return HttpResponse("修改")

class StarkSite(object):
    def __init__(self):
        self._registry = {}


    def register(self,model_class,stark_config_obj = None):
        if not stark_config_obj:
            stark_config_obj = StarkConfig

        self._registry[model_class] = stark_config_obj(model_class,self)



    def get_urls(self):
        urlpatterns = []

        for model_class,stark_config_obj in self._registry.items():
            model_name = model_class._meta.model_name
            app_name = model_class._meta.app_label

            cul_url = url(r'^%s/%s/' %(app_name,model_name),(stark_config_obj.urls,None,None))

            urlpatterns.append(cul_url)

        return urlpatterns

    @property
    def urls(self):
        return (self.get_urls(),None,'stark',)



site = StarkSite()
