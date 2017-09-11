from django.conf.urls import url
from . import views

urlpatterns = [
  url('^register/$',views.register),
  url('^isUnameExist/$',views.isUnameExist),
  url('^add_user/$',views.add_user),
  url('^login/$',views.login),
  url('^send/$',views.send),
  url('^active/$',views.active),
  url('^user_center_info/$',views.user_center_info),
  url('^user_center_order/$',views.user_center_order),
  url('^user_center_site/$',views.user_center_site),
  url('^user_login_verify/$',views.user_login_verify),
]

