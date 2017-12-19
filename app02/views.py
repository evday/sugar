from django.shortcuts import render,redirect
from django.http import QueryDict
from django.db.models import Q

from app02.stark import HostConfigForm

from sugar.pager import Pagination
# Create your views here.
from app02.models import Host
HOST_LIST = []

for i in range(1,105):
    HOST_LIST.append("c%s.com"%i)

def host(request):
    pager_obj = Pagination(request.GET.get('page', 1), len(HOST_LIST), request.path_info,request.GET)
    host_list = HOST_LIST[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()


    params = QueryDict(mutable=True)#设置为True可修改，默认不能修改
    params['_list_filter'] = request.GET.urlencode() #将当前url条件加入到request.GET中
    list_condition = params.urlencode()

    return render(request, 'host.html', {'host_list': host_list, "page_html": html,"list_condition":list_condition})



def user(request):

    if request.method == "POST":
        func_name_str = request.POST.get("list_action")
        pk_list = request.POST.getlist("pk")
        if func_name_str == "批量删除" and pk_list:
            Host.objects.filter(id__in=pk_list).delete()
            return redirect("/user/")





    key_word = request.GET.get("key",'')

    all_host = Host.objects.filter(Q(hostname__icontains=key_word)|Q(ip__icontains=key_word)|Q(port__icontains=key_word))

    pager_obj = Pagination(request.GET.get('page', 1), len(all_host), request.path_info, request.GET)
    user_list = all_host[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    list_condition = request.GET.urlencode()

    params = QueryDict(mutable=True)
    params['_list_filter'] = request.GET.urlencode()
    list_condition = params.urlencode()
    return render(request, 'user.html', {'host_list': user_list, "page_html": html,"list_condition":list_condition,})


def edit(request,id):

    if request.method == "GET":
        obj = Host.objects.get(id=id)
        form = HostConfigForm(instance=obj)
        return render(request,'edit.html',{"form":form})

    else:
        obj = Host.objects.get(id=id)
        form = HostConfigForm(instance=obj,data=request.POST)
        if form.is_valid():
            form.save()
            url = "/user/?%s" % (request.GET.get('_list_filter'))
            return redirect(url)
        return render(request, 'edit.html', {"form": form})
def add(request):
    if request.method == "GET":
        form = HostConfigForm()
        return render(request, 'edit.html', {"form": form})
    else:

        form = HostConfigForm(data=request.POST)
        if form.is_valid():
            form.save()
            url = "/user/?%s" % (request.GET.get('_list_filter'))
            return redirect(url)
        return render(request, 'edit.html', {"form": form})
def delete(request,nid):
    if request.method == "GET":
        return render(request,'my_delete.html')
    else:
        Host.objects.filter(id=nid).delete()
        url = "/user/?%s" % (request.GET.get('_list_filter'))
        return redirect(url)




