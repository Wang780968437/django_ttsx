from django.http import JsonResponse
from django.shortcuts import render
from .models import *
from tt_cart.models import *
from ttsx_user.models import UserInfo

# Create your views here.


# 从购物车提交订单后转到确认订单页面
def verify_order(request):
    # 获取登录用户名
    name = request.session.get('user_name')
    print(name)
    # 获取该用户提交的购物车信息,列表元素是字符串
    cart_ids = request.GET.getlist('cart_id')
    # 遍历转换为数字
    lists = []
    for i in cart_ids:
        lists.append(int(i))

    carts = CartInfo.objects.filter(pk__in=lists)
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
    print(orderinfolist)
    # 上下文
    context = {"list":orderinfolist}
    return render(request,"tt_order/user_center_order.html",context)