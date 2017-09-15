from django.conf.urls import url
from . import views


urlpatterns=[
   url('^detail/$',views.detail)
]