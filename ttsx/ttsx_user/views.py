from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail
from .models import *

# Create your views here.

def register(request):
    return render(request,'ttsx_user/register.html')

def isUnameExist(request):
    uname = request.GET.get('value')
    user_list = UserInfo.objects.all()
    for u in user_list:
        if(u.uname == uname):
            return JsonResponse({'strErr':'此用户名已存在'})

    return JsonResponse({'strErr':''})

def add_user(request):
    user = UserInfo()
    uname = request.POST.get('user_name').strip()
    upwd = request.POST.get('pwd').strip()
    uemail = request.POST.get('email').strip()

    user.uname = uname
    user.upwd = upwd
    user.uemail = uemail
    user.save()

    return redirect('/user/login/')

def login(request):
    return render(request,'ttsx_user/login.html')

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
    user_name = request.POST.get('username')
    user_pwd = request.POST.get('pwd')

    user_list = UserInfo.objects.all()
    for u in user_list:
        if (u.uname == user_name and u.upwd == user_pwd):
            response = redirect('/user/user_center_info/')
            response.set_cookie('name',user_name)
            return response

    return HttpResponse('用户名或密码错误')




