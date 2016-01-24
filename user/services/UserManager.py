from lazysignup.models import LazyUser
from lazysignup.signals import converted
from lazysignup.utils import is_lazy_user
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as log, logout as djangologout

def register(request, username, firstname, lastname, email, passwd):
    user = request.user
    if is_lazy_user(user):
        convert_lazy_user(user, username, email, passwd)
    elif user.is_anonymous():
        user = User.objects.create_user(username, email=email, password=passwd,
                first_name=firstname, last_name=lastname)
    login(request, username, passwd)


def convert_lazy_user(user, username, email, password):
    # TODO: proper error handling of user with the used username (or email,
    # depending what we will use for identification)
    user.username = username
    user.email = email
    user.set_password(password)
    user.backend = None
    user.save()
    LazyUser.objects.filter(user=user).delete()
    converted.send(None, user=user)
    assert is_lazy_user(user) == False


def login(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            if is_lazy_user(request.user):
                LazyUser.objects.filter(user=request.user).delete()
                request.user.delete()
            log(request, user)
            return True
        else:
            return False
    else:
        return False


def logout(request):
    return djangologout(request)


def loggedIn(request):
    if request.user.is_authenticated():
        return request.user.username
    else:
        return None
