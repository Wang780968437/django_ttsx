from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator, Page
from haystack.generic_views import SearchView


# Create your views here.

# 首页
def index(request):
    type_list = TypeInfo.objects.all()
    list = []
    for type in type_list:
        new = type.goodsinfo_set.all().order_by('-id')[0:4]
        click = type.goodsinfo_set.all().order_by('-gclick')[0:3]
        list.append({'type': type, 'new': new, 'click': click})

    context = {'title': '首页', 'iscart': 1, 'list': list}
    return render(request, 'tt_goods/index.html', context)


def list(request, tid, pindex, porder):
    order_str = '-id'
    if porder == '2':
        order_str = '-gprice'
    elif porder == '3':
        order_str = '-gclick'
    glist = GoodsInfo.objects.filter(gtype_id=tid).order_by(order_str)
    gnew = GoodsInfo.objects.filter(gtype_id=tid).order_by('-id')[0:2]
    ttitle = TypeInfo.objects.get(id=tid).ttitle
    paginator = Paginator(glist, 10)
    pindex1 = int(pindex)
    page = paginator.page(pindex1)
    context = {'title': '商品列表', 'iscart': 1, 'page': page, 'new': gnew, 'tid': tid,
               'pindex': pindex1, 'porder': porder, 'ttitle': ttitle}

    return render(request, 'tt_goods/list.html', context)


def detail(request, gid):
    goods = GoodsInfo.objects.get(id=gid)
    goods.gclick = goods.gclick + 1
    goods.save()

    new = goods.gtype.goodsinfo_set.all().order_by('-id')[0:2]
    context = {'title': '商品详情', 'iscart': 1, 'goods': goods, 'new': new}
    response = render(request, 'tt_goods/detail.html', context)

    browse_list = []
    browse_str = request.COOKIES.get('browse', '')
    if browse_str:
        browse_list = browse_str.split(',')
        if gid in browse_list:
            browse_list.remove(gid)
        browse_list.insert(0, gid)
        if len(browse_list) > 5:
            browse_list.pop()
    else:
        browse_list = [gid]

    response.set_cookie('browse', ','.join(browse_list), max_age=60 * 60 * 24 * 7)
    return response


class GoodsSearchView(SearchView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['iscart'] = 1
        context['qwjs'] = 2
        context['title'] = '搜索'
        return context
