from django.conf.urls import url
from . import views


urlpatterns=[
   url(r'^list(\d+)_(\d+)_(\d+)/$',views.list),
   url('^$',views.index),
   url(r'^(\d+)/$',views.detail),
   url('^search/$',views.GoodsSearchView.as_view()),
]
