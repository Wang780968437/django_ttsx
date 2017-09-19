
from django.conf.urls import url
from . import views

urlpatterns = [
  url('^register/$',views.register),
  url('^uname_exist/$',views.uname_exist),
  url('^add_user/$',views.add_user),
  url('^login/$',views.login),
  url(r'^active/$',views.active),
  url('^user_center_info/$',views.user_center_info),
  url('^user_center_order/$',views.user_center_order),
  url('^user_center_site/$',views.user_center_site),
  url('^user_login_verify/$',views.user_login_verify),
  url('^logout/$',views.logout),
  url('^verify_code/$',views.verify_code),
  url('^pwd_handle/$',views.pwd_handle),
]

