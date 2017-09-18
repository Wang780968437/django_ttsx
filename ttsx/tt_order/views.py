
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime
from django.core.paginator import Paginator
from .models import *
from tt_cart.models import *
from ttsx_user import user_decorator
from ttsx_user.models import UserInfo,UserAddressInfo

# Create your views here.

@user_decorator.login
# 从购物车提交订单后转到确认订单页面
def verify_order(request):
    # 获取登录用户名
    uid = request.session.get('user_id')
    # print(uid)
    name = request.session.get('user_name')
    addrs = UserAddressInfo.objects.filter(user_id=uid)
    # print(addrs)
    # 获取该用户提交的购物车信息
    cart_ids = request.GET.getlist('cart_id')
    # print(type(cart_ids))
    carts = CartInfo.objects.filter(pk__in=[1,2,3,4])
    length = len(carts)
    # print(carts)
    context = {'title':'提交订单',
               'cartlist':carts,
               'length':length,
               'uname':name,
               'addrs':addrs,
    }
    return render(request,"tt_order/place_order.html",context)

@transaction.atomic
@user_decorator.login
# 订单列表
def order_list(request):

    uid = request.session.get('user_id')
    addr_id = request.POST.get('addr_id')
    # print(addr_id)
    addr = UserAddressInfo.objects.filter(id=addr_id)
    # print(addr)
    cids = request.POST.getlist('cid')
    print(cids)
    if cids == []:
        return redirect('/cart/')
    #开始事件,保存回退点
    sid = transaction.savepoint()
    # 创建订单对象
    order = OrderInfo()
    order.oid = "%s%s"%(datetime.now().strftime('%Y%m%d%H%M%S'),uid)
    order.user_id = uid
    order.ototal = 0
    order.oaddress =  addr[0].uaddress +' ( '+ addr[0].uname + ' 收' +' ) '+ addr[0].uphone
    order.save()
    # 查询选中的购物车信息
    carts = CartInfo.objects.filter(id__in=cids)
    print(carts)
    total = 0
    isOK = True
    for cart in carts:
        print(cart)
        if cart.count <= cart.goods.gkucun:
            # 库存充足，创建详单对象
            detail = OrderDetailInfo()
            detail.goods = cart.goods
            detail.order = order
            detail.count = cart.count
            detail.price = cart.goods.gprice*cart.count
            detail.save()
            # 计算每条购物车商品的总价格
            total += detail.price
            # 减少库存
            cart.goods.gkucun -= cart.count
            cart.goods.save()
            # 删除购物车对象
            cart.delete()
        else:
            isOK = False
            break

    if isOK:
        # 保存总价
        order.ototal = total + 10
        order.save()
        # 提交
        transaction.savepoint_commit(sid)
        return redirect("/tt_order/all_order/")
        # return JsonResponse({'ok':'ok'})
    else:
        transaction.savepoint_rollback(sid)
        return redirect('/cart/')


@user_decorator.login
# 订单中心
def all_order(request, pindex):
    # 获取登录的用户名
    name = request.session.get('user_name')
    # print(name)
    # 根据当前登陆的用户名，获取用户所有订单信息
    orderinfolist = OrderInfo.objects.filter(user__uname=name).order_by("-oid")
    print(orderinfolist)
    # 全部订单详情列表
    lists = []
    # 定义保存未支付订单列表
    # lists0 = []
    # 定义保存已支付订单列表
    # lists1 = []
    for orderinfo in orderinfolist:
        # 每笔未支付订单
        # if orderinfo.oIsPay == 0:
        detailinfo0 = OrderDetailInfo.objects.filter(order_id=orderinfo.oid)
        lists.append([orderinfo,detailinfo0])
        # else:
            # 每笔已支付订单
            # detailinfo1 = OrderDetailInfo.objects.filter(order_id=orderinfo.oid)
            # lists1.append([orderinfo,detailinfo1])
    # 按全部订单分页，每页显示2条
    paginator = Paginator(lists, 2)
    # 获取页码列表
    plist = paginator.page_range
    if pindex == '':
        pindex='1'
    pindex=int(pindex)
    # 当前页数据
    page = paginator.page(pindex)
    # 上下文
    context = {"uname":name,
               'page':page,
               'plist':plist,
               'pindex':pindex
               }
    return render(request,"tt_order/user_center_order.html",context)

def pay(request):
    oid = request.POST.get("oid")
    print(oid)
    order = OrderInfo.objects.get(oid=oid)
    order.oIsPay = 1
    order.save()
    return render(request,"tt_order/pay.html")

