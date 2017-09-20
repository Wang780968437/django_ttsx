# coding=utf-8
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import *
from ttsx_user.user_decorator import *
from django.db.models import Sum




# Create your views here.

@login
def index(request):
    uid = int(request.session['user_id'])
    cart_list = CartInfo.objects.filter(user_id=uid)
    context = {'title': '购物车', 'isuser': 1, 'clist': cart_list}
    return render(request, 'tt_cart/cart.html', context)


@login
def add(request):
    uid = int(request.session['user_id'])
    gid = int(request.GET.get('gid'))
    count = int(request.GET.get('count'))

    cart_list = CartInfo.objects.filter(goods_id=gid, user_id=uid)
    if cart_list:
        cart = cart_list[0]
        cart.count += count
        cart.save()
    else:
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = gid
        cart.count = count
        cart.save()

    if request.is_ajax():
        # count = CartInfo.objects.filter(user_id=uid).count()
        count = CartInfo.objects.filter(user_id = uid).aggregate(Sum('count'))
        return JsonResponse({'ok': 1, 'count': count.get('count__sum')})

    return redirect('/cart/')


@login
def add_list(request):
    uid = int(request.session['user_id'])
    gid = int(request.GET.get('gid'))

    cart_list = CartInfo.objects.filter(goods_id=gid, user_id=uid)
    if cart_list:
        cart = cart_list[0]
        cart.count += 1
        cart.save()
    else:
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = gid
        cart.count = 1
        cart.save()

    if request.is_ajax():
        # count = CartInfo.objects.filter(user_id=uid).count()
        count = CartInfo.objects.filter(user_id=uid).aggregate(Sum('count'))
        return JsonResponse({'ok': 1, 'count': count.get('count__sum')})

    return redirect('/cart/')


def edit(request):
    dict = request.GET
    count = int(dict.get('count'))
    cid = int(dict.get('cid'))

    cart = CartInfo.objects.get(id=cid)
    cart.count = count
    cart.save()

    return JsonResponse({'ok': 1})


def delete(request):
    cid = int(request.GET.get('cid'))
    cart = CartInfo.objects.get(id=cid)
    cart.delete()

    return JsonResponse({'ok': 1})


def count(request):
    uid = int(request.session.get('user_id'))
    # count = CartInfo.objects.filter(user_id=uid).count()
    count = CartInfo.objects.filter(user_id=uid).aggregate(Sum('count'))
    return JsonResponse({'count':  count.get('count__sum')})
