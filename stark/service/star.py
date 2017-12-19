#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2017-12-14,15:03"
from django.conf.urls import url
from django.utils.safestring import mark_safe
from django.shortcuts import HttpResponse,render,redirect
from django.urls import reverse
from django.forms import ModelForm
from django.http import QueryDict
from django.db.models import Q


from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from sugar.pager import Pagination


class ChangeList(object):

    def __init__(self,config,query_list):
        self.config = config

        self.list_display = config.get_list_display()
        self.model_class = config.model_class
        self.request = config.request
        self.query_list = query_list
        self.show_add_btn = config.get_show_add_btn()
        self.search_key = config.search_key
        self.actions = config.get_actions()
        self.show_actions = config.get_show_actions()

        #搜索
        self.show_search_form = config.get_show_search_form() #是否显示搜索框
        self.search_form_val = config.request.GET.get(config.search_key,'') #获取搜索框里的value

        # 分页功能
        current_page = self.request.GET.get('page', 1)
        total_count = self.query_list.count()
        pager_obj = Pagination(current_page, total_count, self.request.path_info, self.request.GET)

        self.pager_obj = pager_obj

    def modify_actions(self):
        result = []
        for func in self.actions:
            temp = {"name":func.__name__,"text":func.short_desc} # __name__ 取函数名，short_desc 简单描述
            result.append(temp)
        return result



    def head_list(self):
        # 展示表头
        result = []
        for field_name in self.list_display:
            if isinstance(field_name, str):
                # 根据类和字段名称获取字段对象的verbose_name

                # 如果是字段的话，就获取字段的verbose_name
                verbose_name = self.model_class._meta.get_field(field_name).verbose_name
            else:
                # 如果是函数的，就执行函数里面的方法
                verbose_name = field_name(self.config, is_header=True)  # 函数名加括号，调用
            result.append(verbose_name)
        return result

    def body_list(self):
        new_data_list = []
        data_list = self.query_list[self.pager_obj.start:self.pager_obj.end]
        for row in data_list:
            temp = []
            for field_name in self.list_display:
                if isinstance(field_name, str):  # 不是字符串不能用getattr
                    val = getattr(row, field_name)  # 利用字符串去取对象里面的数据用反射
                else:
                    val = field_name(self.config, row)  # 当前对象row传递给obj
                temp.append(val)
            new_data_list.append(temp)
        return new_data_list


    def add_url(self):
        return self.config.get_add_url()



class StarkConfig(object):
    def __init__(self, model_class, site):
        self.model_class = model_class
        self.site = site
        self.request = None
        self._query_params_key = "_list_filter"
        self.search_key = "q"

    list_display = []
    #显示checkbox
    def checkbox(self,obj = None,is_header = False):
        if is_header:
            return '选择'
        return mark_safe("<input type='checkbox' name='pk' value= %s>"%(obj.id,))
    #显示编辑
    def edit(self,obj = None,is_header = False):



        if is_header:
            return "编辑"
        query_str = self.request.GET.urlencode()
        params = QueryDict(mutable=True)
        params[self._query_params_key] = query_str
        return mark_safe("<a href='%s?%s'><button class='btn btn-success'>编辑</button></a>"%(self.get_change_url(obj.id),params.urlencode()))
    #显示删除
    def delete(self,obj = None,is_header = False):
        if is_header:
            return "删除"
        return mark_safe("<a href='%s'><button class='btn btn-danger'>删除</button></a>"%(self.get_delete_url(obj.id)))
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
    show_add_btn = False

    def get_show_add_btn(self):
        return self.show_add_btn
    #ModelFormClass
    model_form_class = None
    def get_model_form_class(self):
        if self.model_form_class:
            return self.model_form_class

        # 方法一
        # class TestModelForm(ModelForm):
        #     class Meta:
        #         model = self.model_class
        #         fields = "__all__"
        # return TestModelForm

        #方法二，利用type生成
        meta = type("Meta",(object,),{"model":self.model_class,"fields":"__all__"})
        TestModelForm = type("TestModelForm",(ModelForm,),{"Meta":meta})
        return TestModelForm

    #关键字搜索
    show_search_form = False

    #是否显示搜索框
    def get_show_search_form(self):
        if self.show_search_form:
            return self.show_search_form

    search_fields = []
    #扩展搜索字段
    def get_search_fields(self):
        result = []
        if self.search_fields:#这个self是自定制config对象
            result.extend(self.search_fields)
        return result

    #搜索条件
    def get_search_condition(self):
        key_words = self.request.GET.get(self.search_key) #搜索内容

        search_fields = self.get_search_fields() #搜索字段

        condition = Q()#实例化Q对象
        condition.connector = "or"
        if key_words and self.get_show_search_form():
            for field_name in search_fields:
                print(field_name,'------------')
                condition.children.append((field_name,key_words))
                print(condition,'999999999999999999999')
        return condition

    def wrapper(self,view_func):
        def inner(request,*args,**kwargs):
            self.request = request
            return view_func(request,*args,**kwargs)
        return inner


    #定制actions
    show_actions = False
    def get_show_actions(self):
        if self.show_actions:
            return self.show_actions

    actions = []
    def get_actions(self):
        result = []
        if self.actions:
            result.extend(self.actions)
        return result



    #动态显示增删改查url
    def get_urls(self):

        app_model_name = (self.model_class._meta.app_label,self.model_class._meta.model_name)
        urlpatterns = [
            url(r'^$',self.wrapper(self.changelist_view),name="%s_%s_changelist" %app_model_name),
            url(r'^add/$',self.wrapper(self.add_view),name="%s_%s_add" %app_model_name),
            url(r'^(\d+)/delete/$',self.wrapper(self.delete_view),name="%s_%s_delete" %app_model_name),
            url(r'^(\d+)/change/$',self.wrapper(self.change_view),name="%s_%s_change" %app_model_name),
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
        if request.method == "POST" and self.get_show_actions():
            func_name_str = request.POST.get("list_action") #取到函数名
            action_func = getattr(self,func_name_str) #利用反射,找到对应的函数
            ret = action_func(request)
            if ret:
                return ret





        query_list = self.model_class.objects.filter(self.get_search_condition())

        c1 = ChangeList(self,query_list)

        return render(request,"stark/classList.html",{"c1":c1})

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

        self.model_class.objects.filter(pk=nid).delete()
        return redirect(self.get_changelist_url())

    #修改页面视图
    def change_view(self, request,nid,*args,**kwargs):

        obj = self.model_class.objects.filter(pk=nid).first()
        model_form_class = self.get_model_form_class()
        if request.method == "GET":
            form = model_form_class(instance=obj)
            return render(request,"stark/change_view.html",{"form":form})
        if request.method == "POST":
            form = model_form_class(instance=obj,data=request.POST)
            if form.is_valid():
                form.save()

                url = request.GET.get(self._query_params_key)
                url_list = "%s?%s"%(self.get_changelist_url(),url)
                return redirect(url_list)
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

'''

eccgw01.boulder.ibm.com
207.25.252.197
'''