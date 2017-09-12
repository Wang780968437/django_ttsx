from django.http import JsonResponse
from django.shortcuts import render
from .models import *

# Create your views here.


# 从购物车提交订单后转到确认订单页面
def verify_order(request):
    goods = request.GET.get("gtitle")

    return render(request,"tt_order/place_order.html")

# 订单列表
def order_list(request):

    return JsonResponse({})


def all_order(request):

    # 判断用户是否登陆

    # 拿到登陆的用户名

    # 根据当前登陆的用户名，获取用户订单信息
    orderinfo = OrderInfo.objects.filter(user__uname='')

    context = {}
    return render(request,"tt_order/user_center_order.html",context)