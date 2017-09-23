# -*- conding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url('^$',views.index),
    url('^order_handle/$',views.order_handle),
]