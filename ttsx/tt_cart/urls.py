from django.conf.urls import url

from . import views

urlpatterns =[
    url('^$',views.index),
    url('^add/$',views.add),
    url('^add_list/$',views.add_list),
    url('^edit/$',views.edit),
    url('^delete/$',views.delete),
    url('^count/$',views.count),
]
