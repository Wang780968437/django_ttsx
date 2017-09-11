from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def show_cart(request):
    return render(request, 'tt_cart/cart.html')


def detail(request):
    return render(request, 'tt_goods/detail.html')

def add_cart(request):
    good_name = request.GET.get('$good_name')
    show_pirze = request.GET.get('$show_pirze')
    num_show = request.GET.get('$num_show')
    goods_detail_pic = request.GET.get('$goods_detail_pic')
    context = {'good_name': good_name, 'show_pirze': show_pirze, 'num_show': num_show, 'goods_detail_pic': goods_detail_pic}

    return render(request, 'tt_cart/cart.html', context)