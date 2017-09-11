# -*- conding: utf-8 -*-
from django.conf.urls import url

from tt_order import views

urlpatterns = [
    url(r'to_pay/$',views.verify_order),
    url(r'order_list/$',views.order_list),
    url(r'all_order/$',views.all_order)
]