from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

from tt_goods.models import GoodsInfo
from .models import *
from ttsx_user.user_decorator import login

# Create your views here.
@login
def show_cart(request):
    # 获取该用户的所有购物车表中的数据
    uid = request.session.get('user_id')
    cart_info = CartInfo.objects.filter(user_id=uid)
    context = {'cart_info': cart_info, 'title': '购物车', 'dd': 2}
    return render(request, 'tt_cart/cart.html', context)


@login
# 添加到购物车
def add_cart(request):
    # 用户id
    user_id = request.session.get('user_id')
    # 食品id
    goods_id = request.GET.get('id')

    # 食品数量
    counter = request.GET.get('counter')
    # 获取该用户所有的订单
    cart_list = CartInfo.objects.filter(user_id=user_id)
    # 判断是否有该物品(减少访问数据库)
    # 缓存：(使用变量保存)查询集的结果被存下来之后，再次查询时会使用之前缓存的数据
    carts = cart_list.filter(goods_id=goods_id)
    if carts:
        # 取出第一条数据
        carts[0].count += int(counter)
        carts[0].goods.gclick += 1
        carts[0].save()
    else:

        if goods_id:
            # 在购物车保存一条数据
            cart = CartInfo()
            cart.user_id = user_id
            cart.goods_id = goods_id
            cart.count = int(counter)
            # 食品点击量+1
            cart.goods.gclick += 1
            cart.save()
    return JsonResponse({'num': cart_list.count()})

# 购物车删除数据
def delete_goods(request):
    cart_id = request.GET.get('cart_id')
    cart = CartInfo.objects.get(id=cart_id)
    cart.delete()
    return JsonResponse({'ok': 'ok'})


# 购物车文本修改数据
def edit(request):
    num = request.GET.get('num')
    cid = request.GET.get('cid')
    cart = CartInfo.objects.get(id=cid)
    cart.count = num
    cart.save()
    return JsonResponse({'ok': 'ok'})

