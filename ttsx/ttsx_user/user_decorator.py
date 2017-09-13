#!/user/bin/env python3
# -*- conding:utf-8 -*-

from django.http import HttpResponseRedirect

def login(func):
    def login_fun(request,*args,**kwargs):
        if request.session.has_key('user_id'):
            return func(request,*args,**kwargs)
        else:
            response = HttpResponseRedirect('/user/login/')
            response.set_cookie('url',request.get_full_path())
            return response

    return login_fun

