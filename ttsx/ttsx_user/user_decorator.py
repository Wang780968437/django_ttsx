#!/user/bin/env python3
# -*- conding:utf-8 -*-

from django.shortcuts import redirect
from django.http import JsonResponse


def login(func):
    def login_fun(request,*args,**kwargs):
        if 'user_id' in request.session:
            return func(request,*args,**kwargs)
        else:
            # response = HttpResponseRedirect('/user/login/')
            # response.set_cookie('url',request.get_full_path())
            # return response

            if request.is_ajax():
                return JsonResponse({'login':1})

            return redirect('/user/login/')

    return login_fun

