from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from functools import wraps


def teacher_required(view_func):
    @login_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        profile = getattr(request.user, 'profile', None)
        if profile is None or profile.role != 'teacher':
            return redirect('course_list')
        return view_func(request, *args, **kwargs)
    return wrapper