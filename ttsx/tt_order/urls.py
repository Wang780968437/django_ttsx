# -*- conding: utf-8 -*-
from django.conf.urls import url

from tt_order import views

urlpatterns = [
    url(r'to_pay/$',views.show_order),
]