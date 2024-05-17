# from functools import wraps
# from django.shortcuts import redirect

# def admin_required(view_func):
#     @wraps(view_func)
#     def _wrapped_view(request, *args, **kwargs):
#         if request.user.is_authenticated and request.user.is_staff:
#             return view_func(request, *args, **kwargs)
#         else:
#             return redirect('login')  # Replace 'login' with the name/url of your login view
#     return _wrapped_view

from django.contrib.auth.decorators import user_passes_test

def group_required(group_name):
    def in_group(user):
        return user.groups.filter(name=group_name).exists() or user.is_superuser
    return user_passes_test(in_group)