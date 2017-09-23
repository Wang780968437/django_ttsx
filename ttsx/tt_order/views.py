from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime
from django.core.paginator import Paginator
from .models import *
from tt_cart.models import *
from ttsx_user.user_decorator import *
from ttsx_user.models import *
from django.db import transaction


# Create your views here.

@login
def index(request):
    dict = request.GET
    uid = int(request.session.get('user_id'))
    address = UserAddressInfo.objects.get(user_id=uid)
    cid_list = dict.getlist('cid')
    cart_list = CartInfo.objects.filter(id__in=cid_list)
    context = {'title': '提交订单', 'isuser': 1, 'cart_list': cart_list, 'address': address}
    return render(request, 'tt_order/place_order.html', context)


@transaction.atomic
def order_handle(request):
    dict = request.POST
    cid_list = dict.getlist('cid')
    address = dict.get('address')
    uid = int(request.session.get('user_id'))

    sid = transaction.savepoint()
    order = OrderInfo()
    order.oid = '%s%d'%(datetime.now().strftime('%Y%m%d%H%M%S'), uid)
    order.user_id = uid
    order.ototal = 0
    order.oaddress = address
    order.save()

    total = 0
    isOk = True
    cart_list = CartInfo.objects.filter(id__in=cid_list)
    for cart in cart_list:
        if cart.count <= cart.goods.gkucun:
            detail_order = OrderDetailInfo()
            detail_order.goods = cart.goods
            detail_order.order = order
            detail_order.price = cart.goods.gprice
            detail_order.count = cart.count
            detail_order.save()

            total += detail_order.price * detail_order.count
            cart.goods.gkucun -= cart.count
            cart.goods.save()
            cart.delete()
        else:
            isOk = False
            break

    if isOk:
        order.ototal = total
        order.save()
        transaction.savepoint_commit(sid)
        return redirect('/user/user_center_order/')
    else:
        transaction.savepoint_rollback(sid)
        return redirect('/cart/')






