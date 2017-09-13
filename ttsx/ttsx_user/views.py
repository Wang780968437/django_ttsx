# coding=utf-8
from PIL import Image,ImageDraw, ImageFont
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail
from hashlib import sha1
from .models import *
from . import user_decorator

# Create your views here.

def register(request):
    return render(request,'ttsx_user/register.html',{'title':'注册'})

def uname_exist(request):
    name = request.GET.get('name')
    count = UserInfo.objects.filter(uname = name).count()

    return JsonResponse({'count':count})

def add_user(request):
    user = UserInfo()
    uname = request.POST.get('user_name').strip()
    upwd = request.POST.get('pwd').strip()
    uemail = request.POST.get('email').strip()

    s1 = sha1()
    s1.update(upwd.encode('utf-8'))
    supwd = s1.hexdigest()

    user.uname = uname
    user.upwd = supwd
    user.uemail = uemail
    user.save()

    msg = '<a href="http://127.0.0.1:8000/user/active%s/" target="_blank">点击激活</a>'%(user.id)
    send_mail('天天生鲜用户激活', '',
              settings.EMAIL_FROM,
              [uemail],
              html_message=msg)

    # return HttpResponse('用户注册成功，请到邮箱中激活！')
    return redirect('/user/login_1/')

def login_1(request):
    uname = request.COOKIES.get('uname','')
    context = {'title':'用户登陆', 'error_name':0, 'error_pwd':0, 'error_yzm':0, 'uname': uname}
    return render(request, 'ttsx_user/login_1.html', context)


def active(request,uid):
    user = UserInfo.objects.get(id = uid)
    user.isActive = True
    user.save()
    return HttpResponse('激活成功，<a href="/user/login/">点击登录</a>')

def login(request):
    uname = request.COOKIES.get('uname','')
    context = {'title':'用户登陆', 'error_name':0, 'error_pwd':0, 'error_yzm':0, 'uname': uname}
    return render(request, 'ttsx_user/login.html', context)

@user_decorator.login
def user_center_info(request):
    user_email = UserInfo.objects.get(id = request.session['user_id']).uemail
    context = {'title':'用户中心', 'user_email':user_email, 'user_name':request.session['user_name']}
    return render(request, 'ttsx_user/user_center_info.html',context)

@user_decorator.login
def user_center_order(request):
    context = {'title':'用户中心'}
    return render(request, 'ttsx_user/user_center_order.html',context)

@user_decorator.login
def user_center_site(request):
    userId = request.session['user_id']
    count = UserAddressInfo.objects.filter(user_id = userId).count()
    if count == 0:
        if request.method == 'POST':
            u_info = UserAddressInfo()
            post = request.POST
            u_info.uname = post.get('user')
            u_info.uaddress = post.get('uaddress')
            u_info.uphone = post.get('uphone')
            u_info.user_id = userId
            u_info.ucode = post.get('ucode')
            u_info.save()
            count = 1
            context = {'title': '用户中心', 'user': u_info,'count':count}
            return render(request, 'ttsx_user/user_center_site.html', context)
        else:
            return render(request, 'ttsx_user/user_center_site.html', {'title': '用户中心','count':count})
    else:
        u_info = UserAddressInfo.objects.get(user_id=userId)
        if request.method == 'GET':
            context = {'title': '用户中心', 'user': u_info,'count':count}
            return render(request, 'ttsx_user/user_center_site.html', context)
        else:
            post = request.POST
            u_info.uname = post.get('user')
            u_info.uaddress = post.get('uaddress')
            u_info.uphone = post.get('uphone')
            u_info.user_id = userId
            u_info.ucode = post.get('ucode')
            u_info.save()
            context = {'title': '用户中心', 'user': u_info, 'count': count}
            return render(request, 'ttsx_user/user_center_site.html', context)

def user_login_verify(request):
    post = request.POST
    name = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu',0)
    yzm_value = post.get('yzm_value')

    if yzm_value.lower() == request.session['verifycode'].lower():
        users = UserInfo.objects.filter(uname = name)
        if len(users) == 1:
            s1 = sha1()
            s1.update(upwd.encode('utf-8'))
            supwd = s1.hexdigest()
            if supwd == users[0].upwd:
                url = request.COOKIES.get('url','/')
                response = HttpResponseRedirect(url)
                if jizhu != 0:
                    response.set_cookie('uname',name)
                else:
                    response.set_cookie('uname','',max_age=-1)
                request.session['user_id'] = users[0].id
                request.session['user_name'] = name
                return response

            else:
                context = {'title':'登陆','error_name':0,'error_pwd':1, 'error_yzm':0, 'uname':name, 'upwd':upwd}
                return render(request,'ttsx_user/login.html',context)

        else:
            context = {'title': '登陆', 'error_name': 1, 'error_pwd':0, 'error_yzm':0, 'uname': name, 'upwd': upwd}
            return render(request, 'ttsx_user/login.html', context)
    else:
        context =  {'title': '登陆', 'error_name':0, 'error_pwd':0,  'error_yzm':1, 'uname': name, 'upwd': upwd}
        return render(request, 'ttsx_user/login.html', context)

def logout(request):
    request.session.flush()
    return redirect('/user/')

def index(request):
    return render(request,'ttsx_user/index.html',{'title':'首页'})

def verify_code(request):
    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('FreeMono.ttf', 23)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str

    # 内存文件操作(python3)
    from io import BytesIO
    buf = BytesIO()

    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')







