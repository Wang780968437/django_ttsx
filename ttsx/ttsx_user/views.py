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
from . import task
from tt_goods.models import *
from tt_order.models import *
from django.core.paginator import Paginator,Page

# Create your views here.


# 注册
def register(request):
    return render(request,'ttsx_user/register.html',{'title':'注册'})

# 注册时判断用户名是否存在
def uname_exist(request):
    name = request.GET.get('u_name')
    count = UserInfo.objects.filter(uname = name).count()

    return JsonResponse({'count':count})

# 用户注册处理，信息保存
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

    '''
        用task必须在终端先启动redis服务：sudo service redis start
        并且在虚拟环境中项目目录下启动worker：python manage.py celery worker --loglevel=info
        邮件才能发送成功！
    '''
    task.sendmail.delay(user.id, uemail)

    # msg = '<a href="http://127.0.0.1:8000/user/active%s/" target="_blank">点击激活</a>'%(user.id)
    # send_mail('天天生鲜用户激活', '',
    #           settings.EMAIL_FROM,
    #           [uemail],
    #           html_message=msg)

    return HttpResponse('用户注册成功，请到邮箱中激活！')

# 用户通过邮件激活
def active(request,uid):
    user = UserInfo.objects.get(id = uid)
    user.isActive = True
    user.save()
    return HttpResponse('激活成功，<a href="/user/login/">点击登录</a>')

# 登陆
def login(request):
    uname = request.COOKIES.get('uname','')    # 记住用户名
    context = {'title':'登陆', 'uname': uname, 'error_name':0, 'error_pwd':0, 'error_yzm':0}
    return render(request, 'ttsx_user/login.html', context)

# 用户信息
@user_decorator.login
def user_center_info(request):
    user_email = UserInfo.objects.get(id = request.session['user_id']).uemail
    browse_str = request.COOKIES.get('browse', '')
    browse_list = []
    if browse_str:
        list = browse_str.split(',')
        for goods_id in list:
            browse_list.append(GoodsInfo.objects.get(id=int(goods_id)))

    context = {'title':'用户中心', 'user_email':user_email, 'user_name':request.session['user_name'], 'list':browse_list}
    return render(request, 'ttsx_user/user_center_info.html',context)

# 用户所有订单
@user_decorator.login
def user_center_order(request):
    pindex = request.GET.get('page', '1')
    uid = int(request.session.get('user_id'))
    orders = OrderInfo.objects.filter(user_id = uid).order_by('oIsPay','-oid')
    paginator = Paginator(orders, 2)
    page = paginator.page(int(pindex))

    context = {'title':'用户中心', 'page':page}
    return render(request, 'ttsx_user/user_center_order.html',context)

# 用户地址信息
@user_decorator.login
def user_center_site(request):
    userId = request.session['user_id']

    # 判断用户是否添加过地址
    count = UserAddressInfo.objects.filter(user_id = userId).count()

    # 没有添加，根据请求方式POST，GET分别处理
    if count == 0:
        # POST请求，保存表单数据到表中，把count=1表示用户已添加地址
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
        else:# GET 请求直接跳转
            return render(request, 'ttsx_user/user_center_site.html', {'title': '用户中心','count':count})

    else:  # 用户已经添加地址，GET 请求直接显示，POST请求，保存用户的修改，显示修改后的新地址
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

# 登陆验证
def user_login_verify(request):
    if request.method == 'GET':
        return redirect('/user/login/')

    post = request.POST
    name = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu',0)
    yzm_value = post.get('yzm_value')
    context = {'title':'登陆',  'uname':name, 'upwd':upwd, 'error_name':0, 'error_pwd':0, 'error_yzm':0}

    if yzm_value.lower() == request.session['verifycode'].lower():
        users = UserInfo.objects.filter(uname = name)     #  验证用户是否存在
        if users:
            s1 = sha1()
            s1.update(upwd.encode('utf-8'))
            supwd = s1.hexdigest()
            if supwd == users[0].upwd:
                if users[0].isActive:
                    url = request.session.get('url','/')
                    response = HttpResponseRedirect(url)
                    if jizhu != 0:
                        response.set_cookie('uname',name,max_age=60*60*24*7)
                    else:
                        response.set_cookie('uname','',max_age=-1)
                    request.session['user_id'] = users[0].id
                    request.session['user_name'] = name
                    return response      #   登陆成功时的跳转
                else:
                    return HttpResponse('请先到邮箱中激活再回来登陆!')

            else: #   密码错误时的处理
                context['error_pwd'] = 1
                return render(request,'ttsx_user/login.html',context)

        else:   #   用户名错误时的处理
            context['error_name'] = 1
            return render(request, 'ttsx_user/login.html', context)

    else:  #验证码错误时的处理
        context['error_yzm'] = 1
        return render(request, 'ttsx_user/login.html', context)

# 退出登陆
def logout(request):
    request.session.flush()
    response = HttpResponseRedirect('/')
    response.delete_cookie('browse')
    # response.delete_cookie('url')
    return response

# 生成验证码
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

# 修改密码
def pwd_handle(request):
    dict = request.POST
    new_pwd = dict.get('newPwd')

    u_name = request.session['user_name']
    user = UserInfo.objects.get(uname=u_name)

    s1 = sha1()
    s1.update(new_pwd.encode('utf-8'))
    supwd = s1.hexdigest()

    user.upwd = supwd
    user.save()
    request.session.flush()
    response = HttpResponseRedirect('/user/login/')
    response.set_cookie('url','/user/user_center_info/')
    return response

@user_decorator.login
def site(request):
    pass

@user_decorator.login
def site_handle(request):
    post = request.POST
    uid = request.session.get('user_id')
    uname = post.get('user')
    uaddress = post.get('uaddress')
    uphone = post.get('uphone')
    ucode = post.get('ucode')

    addresee = UserAddressInfo()
    addresee.uname = uname
    addresee.user_id = uid
    addresee.uphone = uphone
    addresee.ucode = ucode
    addresee.uaddress = uaddress
    addresee.save()

    context = {'title': '用户中心'}
    return render(request,'ttsx_user/user_center_site1.html', context)












