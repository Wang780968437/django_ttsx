
class GetPathMiddleware:
    def process_view(self, request, view_func, view_args, view_kwargs):
        no_path = [
            '/user/register/',
            '/user/uname_exist/',
            '/user/add_user/',
            '/user/login/',
            '/user/user_login_verify/',
            '/user/logout/',
            '/user/verify_code/',
            '/user/pwd_handle/'
        ]

        if request.path not in no_path:
           request.session['url'] = request.get_full_path()
