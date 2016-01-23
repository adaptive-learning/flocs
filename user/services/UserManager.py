from lazysignup.models import LazyUser
from lazysignup.signals import converted
from lazysignup.utils import is_lazy_user
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as log, logout as djangologout

def register(request, username, firstname, lastname, email, passwd):
    user = request.user
    if is_lazy_user(user):
        user.username = username
        user.email = email
        user.set_password(passwd)
        user.save()
        LazyUser.objects.filter(user=user).delete()
        converted.send(None, user=user)
    elif user.is_anonymous():
        user = User.objects.create_user(username, email=email, password=passwd,
                first_name=firstname, last_name=lastname)
    login(request, username, passwd)


def login(request, username, password):
    if is_lazy_user(request.user):
        LazyUser.objects.filter(user=request.user).delete()
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
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
