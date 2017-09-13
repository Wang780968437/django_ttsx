from django.http import JsonResponse
from django.shortcuts import render
from .models import *
from tt_cart.models import *
from ttsx_user.models import UserInfo

# Create your views here.


# 从购物车提交订单后转到确认订单页面
def verify_order(request):
    # 获取登录用户id
    uid = request.session.get('user_id')
    print(uid)
    # 获取该用户购物车
    carts = CartInfo.objects.filter(user_id = uid)
    print(carts)
    context = {'cartlist':carts}


    return render(request,"tt_order/place_order.html",context)

# 订单列表
def order_list(request):

    return JsonResponse({'ok':'ok'})

# 订单中心
def all_order(request):

    # 获取登录的用户名
    name=request.session.get('user_name')
    print(name)
    # 根据当前登陆的用户名，获取用户所有订单信息
    orderinfolist = OrderInfo.objects.filter(user__uname = name)
    # 上下文
    context = {"list":orderinfolist}
    return render(request,"tt_order/user_center_order.html",context)