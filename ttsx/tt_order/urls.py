# -*- conding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^to_pay/$',views.verify_order),
    url(r'^order_list/$',views.order_list),
    # url(r'^all_order/$',views.all_order),
    url(r'^all_order(\d*)/$', views.all_order),
    url(r'^pay/$',views.pay),
]