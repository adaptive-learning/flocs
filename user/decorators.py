from functools import wraps
from django.utils.decorators import available_attrs
from django.http import HttpResponse
from lazysignup.utils import is_lazy_user


def user_passes_test(test_func, error_func):
    """
    Decorator for views that checks that the user passes the given test,
    calling given error handling callable if necessary. The test should be
    a callable that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            return error_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def login_required(view_func=None, error_func=None):
    """
    Decorator for views that checks that the user is logged in, returning 401
    status if necessary.
    """
    if not error_func:
        error_func = respond_unauthorised

    actual_decorator = user_passes_test(
        check_user_login,
        error_func
    )

    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


def staff_member_required(view_func=None, error_func=None):
    """
    Decorator for views that checks that the user is logged in and is a staff
    member, returning 401 or 403 statuses if necessary.
    """
    if not error_func:
        error_func = respond_forbidden

    actual_decorator = user_passes_test(
        check_user_is_staff,
        error_func
    )

    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


def check_user_login(user):
    return user.is_authenticated() and not is_lazy_user(user)


def check_user_is_staff(user):
    return user.is_active and user.is_staff


def respond_unauthorised(*args, **kwargs):
    return HttpResponse('API call unauthorised, login first.', status=401)


def respond_forbidden(*args, **kwargs):
    return HttpResponse('API call forbidden, insufficient rights', status=403)
