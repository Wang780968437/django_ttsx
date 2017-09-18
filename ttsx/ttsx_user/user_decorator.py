#!/user/bin/env python3
# -*- conding:utf-8 -*-

from django.shortcuts import redirect


def login(func):
    def login_fun(request,*args,**kwargs):
        if 'user_id' in request.session:
            return func(request,*args,**kwargs)
        else:
            # response = HttpResponseRedirect('/user/login/')
            # response.set_cookie('url',request.get_full_path())
            # return response

            return redirect('/user/login/')

    return login_fun

