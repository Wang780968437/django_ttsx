#coding=utf-8
from django.http import JsonResponse
from django.shortcuts import render,redirect
from .models import *
# from ttsx_user import user_decorator
# Create your views here.

# @user_decorator.lohin
def index(request):
    uid=request.session['user_id']
    carts=CartInfo.objects.filter(user_id=uid)
    context ={'title':'购物车',
              'page_name':1,
              'carts':carts}

    return render(request, 'tt_cart/cart.html',context)

# @user_decorator.login
def add(request,gid,count):
    uid=request.session['user_id']
    gid=int(gid)
    count=int(count)
    # 判断用户是否已经购买过此类商品，如果已经购买过则数量增加，否则的话则新增
    carts=CartInfo.objects.filter(user_id=uid,gid_id=gid)
    if len(carts) >= 1:
        cart=carts[0]
        cart.count = cart.count + count
    else:
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = gid
        cart.count = count
    cart.save()
    # 如果是ajax请求列则返回json，否则返回到购物车
    if request.is_ajax():
        count=CartInfo.objects.filter(user_id=request.session['user_id']).cont()
        return JsonResponse({'count':count})
    else:
        return redirect('/cart/')

# @user_decorator.login
def edit(request,cart_id,count):
    try:
        cart=CartInfo.objects.get(pk=(cart_id))
        count1=cart.count=int(count)
        cart.save()
        data={'ok':0}
    except Exception as e:
        data={'ok':count1}
    return JsonResponse(data)

# @user_decorator.login
def delete(request,cart_id):
    try:
        cart=CartInfo.objects.get(pk=(cart_id))
        cart.delete()
        data={'ok':1}
    except Exception as e:
        data={'ok':0}
    return JsonResponse(data)

