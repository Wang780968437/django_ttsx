from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail
from hashlib import sha1
from .models import *

# Create your views here.

def register(request):
    return render(request,'ttsx_user/register.html')

def uname_exist(request):
    name = request.GET.get('name')
    count = UserInfo.objects.filter(uname = name).count()

    return JsonResponse({'count':count})

def add_user(request):
    user = UserInfo()
    uname = request.POST.get('user_name').strip()
    upwd = request.POST.get('pwd').strip().encode()
    uemail = request.POST.get('email').strip()

    s1 = sha1()
    s1.update(upwd)
    supwd = s1.hexdigest()

    user.uname = uname
    user.upwd = supwd
    user.uemail = uemail
    user.save()

    return redirect('/user/login/')

def login(request):
    uname = request.COOKIES.get('uname','')
    context = {'title':'用户登陆', 'error_name':0, 'error_pwd':0, 'uname': uname}
    return render(request, 'ttsx_user/login.html', context)

def send(request):
    msg='<a href="http://127.0.0.1/active/" target="_blank">点击激活</a>'
    send_mail('注册激活','',settings.EMAIL_FROM,
              ['itcast88@163.com'],
              html_message=msg)
    return HttpResponse('ok')

def active(request):
    return HttpResponse('激活')

def user_center_info(request):
    return render(request, 'ttsx_user/user_center_info.html')

def user_center_order(request):
    return render(request, 'ttsx_user/user_center_order.html')

def user_center_site(request):
    return render(request, 'ttsx_user/user_center_site.html')

def user_login_verify(request):
    post = request.POST
    name = post.get('username')
    upwd = post.get('pwd').encode()
    jizhu = post.get('jizhu',0)

    users = UserInfo.objects.filter(uname = name)
    if len(users) == 1:
        s1 = sha1()
        s1.update(upwd)
        supwd = s1.hexdigest()
        if supwd == users[0].upwd:
            response = HttpResponseRedirect('/user/user_center_info/')
            if jizhu != 0:
                response.set_cookie('uname',name)
            else:
                response.set_cookie('uname','',max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = name
            return response

        else:
            context = {'title':'用户登陆','error_name':0,'error_pwd':1,'uname':name,'upwd':upwd}
            return render(request,'ttsx_user/login.html',context)

    else:
        context = {'title': '用户登陆', 'error_name': 1, 'error_pwd': 0, 'uname': name, 'upwd': upwd}
        return render(request, 'ttsx_user/login.html', context)



