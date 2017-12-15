#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2017-12-14,15:03"
from django.conf.urls import url
from django.utils.safestring import mark_safe
from django.shortcuts import HttpResponse,render,redirect
from django.urls import reverse
from django.forms import ModelForm




class StarkConfig(object):
    def __init__(self, model_class, site):
        self.model_class = model_class
        self.site = site

    list_display = []

    #显示checkbox
    def checkbox(self,obj = None,is_header = False):
        if is_header:
            return '选择'
        return mark_safe("<input type='checkbox' name='pk' val= %s>"%(obj.id,))
    #显示编辑
    def edit(self,obj = None,is_header = False):
        if is_header:
            return "编辑"
        return mark_safe("<a href='%s'>编辑</a>"%(self.get_change_url(obj.id)))
    #显示删除
    def delete(self,obj = None,is_header = False):
        if is_header:
            return "删除"
        return mark_safe("<a href='%s'>删除</a>"%(self.get_delete_url(obj.id)))
    #显示增加
    def add(self,obj = None,is_header = False):
        if is_header:
            return "增加"
        return mark_safe("<a href='%s'>增加</a>"%(self.get_add_url()))

    #配置list_display
    def get_list_display(self):
        data = []
        if self.list_display:
            data.extend(self.list_display)
            data.append(StarkConfig.edit)
            data.append(StarkConfig.delete)
            data.insert(0,StarkConfig.checkbox)
        return data

    #是否显示增加按钮
    show_add_btn = True

    def get_show_add_btn(self):
        return self.show_add_btn

    #ModelFormClass
    model_form_class = None
    def get_model_form_class(self):
        if self.model_form_class:
            return self.model_form_class

        #方法一
        # class TestModelForm(ModelForm):
        #     class Meta:
        #         model = self.model_class
        #         fields = "__all__"

        #方法二，利用type生成
        meta = type("Meta",(object,),{"model":self.model_class,"fields":"__all__"})
        TestModelForm = type("TestModelForm",(ModelForm,),{"Meta":meta})
        return TestModelForm


    #动态显示增删改查url
    def get_urls(self):

        app_model_name = (self.model_class._meta.app_label,self.model_class._meta.model_name)
        urlpatterns = [
            url(r'^$',self.changelist_view,name="%s_%s_changelist" %app_model_name),
            url(r'^add/$',self.add_view,name="%s_%s_add" %app_model_name),
            url(r'^(\d+)/delete/$',self.delete_view,name="%s_%s_delete" %app_model_name),
            url(r'^(\d+)/change/$',self.change_view,name="%s_%s_change" %app_model_name),
        ]

        urlpatterns.extend(self.extra_url())

        return urlpatterns

    #反向生成修改页面url
    def get_change_url(self,nid):
        name = 'stark:%s_%s_change'%(self.model_class._meta.app_label,self.model_class._meta.model_name)
        edit_url = reverse(name,args=(nid,))
        return edit_url
    # 反向生成增加页面url
    def get_add_url(self):
        name = 'stark:%s_%s_add'%(self.model_class._meta.app_label,self.model_class._meta.model_name)
        add_url = reverse(name)
        return add_url
    # 反向生成删除页面url
    def get_delete_url(self,nid):
        name = 'stark:%s_%s_delete'%(self.model_class._meta.app_label,self.model_class._meta.model_name)
        delete_url = reverse(name,args=(nid,))
        return delete_url
    #反向生成列表页面url
    def get_changelist_url(self):
        name = 'stark:%s_%s_changelist'%(self.model_class._meta.app_label,self.model_class._meta.model_name)
        changelist_url = reverse(name)
        return changelist_url

    #扩展除增删改查之外的url
    def extra_url(self):
        return []



    @property #property 让类方法伪装成静态字段，可以不加括号就被调用
    def urls(self):
        return self.get_urls()

    #列表页面视图
    def changelist_view(self,request,*args,**kwargs):

        #展示表头
        head_list = []
        for field_name in self.get_list_display():
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
            for field_name in self.get_list_display():
                if isinstance(field_name,str): #不是字符串不能用getattr
                    val = getattr(row,field_name)#利用字符串去取对象里面的数据用反射
                else:
                    val = field_name(self,row) #当前对象row传递给obj
                temp.append(val)
            new_data_list.append(temp)



        return render(request,"stark/classList.html",{"new_data_list":new_data_list,"head_list":head_list,"add_url":self.get_add_url(),"show_add_btn":self.get_show_add_btn()})

    #添加页面视图
    def add_view(self,request,*args,**kwargs):
        model_form_class = self.get_model_form_class()
        if request.method == "GET":
            form = model_form_class()

            return render(request,'stark/add_view.html',{"form":form})

        if request.method == "POST":
            form = model_form_class(request.POST)
            if form.is_valid():
                form.save()
                return redirect(self.get_changelist_url())
            else:
                return render(request, 'stark/add_view.html', {"form": form})

    #删除页面视图
    def delete_view(self, request,nid, *args, **kwargs):
        return HttpResponse("删除")

    #修改页面视图
    def change_view(self, request, nid,*args, **kwargs):

        obj = self.model_class.objects.filter(pk=nid).first()
        model_form_class = self.get_model_form_class()
        if request.method == "GET":
            form = model_form_class(instance=obj)
            return render(request,"stark/change_view.html",{"form":form})
        if request.method == "POST":
            form = model_form_class(instance=obj,data=request.POST)
            if form.is_valid():
                form.save()
                return redirect(self.get_changelist_url())
            return render(request, "stark/change_view.html", {"form": form})

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

