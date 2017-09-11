from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^show_cart/$', views.show_cart),
    url(r'^add_cart/$', views.add_cart),
    url(r'^detail/$', views.detail),
]

