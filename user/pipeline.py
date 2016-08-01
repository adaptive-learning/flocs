from lazysignup.utils import is_lazy_user
from lazysignup.models import LazyUser
from user.services.user_service import delete_lazy_user
from django.contrib.auth import login, logout


def remove_current_user(backend, uid, user=None, *args, **kwargs):
    """
    Handles cases where there was a user loged in (or lazy user) when the
    social authentication started. Normal users are logged out. Lazy users are
    kept, if and only if social account has not yet been used.
    """
    # if there was a user, force login because social auth won't do it
    force_login = user is not None
    request = backend.strategy.request
    provider = backend.name
    social = backend.strategy.storage.user.get_social_auth(provider, uid)
    if social:
        if user and social.user != user:
            if is_lazy_user(user):
                # delete lazy user, if he is to be forgotten anyway
                LazyUser.objects.filter(user=user).delete()
                user.delete()
            else:
                logout(request)
            user = None
    else:
        if user:
            if is_lazy_user(user):
                delete_lazy_user(user)
            else:
                logout(request)
                user = None
    return {'user': user,
            'force_login': force_login}


def manual_login(backend, uid, user=None, force_login=False, *args, **kwargs):
    """
    Due to custom behaviour regarding user already present in time of social
    login, this function will force log in of the social user if required.
    """
    if force_login:
        # backed is especially needed in cases where lazy users are converted
        # to social ones, otherwise they are still treated as lazy
        user.backend = '{0}.{1}'.format(backend.__module__,
                                        backend.__class__.__name__)
        login(backend.strategy.request, user)
    return None
