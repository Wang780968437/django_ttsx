from django.conf.urls import url

from . import views
urlpatterns = [
    url(r'show_cart/$', views.show_cart),
    # 添加到购物车
    url(r'^add_cart/$', views.add_cart),
    # 从购物车删除商品
    url(r'^delete_goods/$', views.delete_goods),
    # 购物车输入框修改
    url(r'^edit/$', views.edit),
]


