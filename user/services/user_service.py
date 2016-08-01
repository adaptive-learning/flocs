from lazysignup.models import LazyUser
from lazysignup.signals import converted
from lazysignup.utils import is_lazy_user
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import authenticate
from django.contrib.auth import login as djangologin, logout as djangologout
from social.apps.django_app.default.models import UserSocialAuth


def signup(request, username, firstname, lastname, email, password):
    # check is username is still available
    qs = User.objects.filter(username=username)
    if qs:
        return None

    user = request.user
    if is_lazy_user(user):
        convert_lazy_user(user, username, email, password)
    else:
        User.objects.create_user(username, email=email, password=password,
                                 first_name=firstname, last_name=lastname)
    # TODO: what if login fails?
    user = login(request, username, password)
    return user


def convert_lazy_user(user, username, email, password):
    # check is username is still available
    qs = User.objects.filter(username=username)
    if qs:
        return None

    user.username = username
    user.email = email
    user.set_password(password)
    user.backend = None
    user.save()
    delete_lazy_user(user)
    assert not is_lazy_user(user)


def delete_lazy_user(user):
    qs = LazyUser.objects.filter(user=user)
    print(qs)
    if qs:
        qs.delete()
        LazyUser.objects.update()
        converted.send(None, user=user)
    # remove lazy sign up backend
    user.backend = None
    user.save()
    assert not is_lazy_user(user)


def login(request, username, password):
    user = authenticate(username=username, password=password)
    # TODO: properly handle these scenarios
    if user is None:
        return None
    if not user.is_active:
        return None

    # TODO: Throws away any progress made befor login, this should probably
    # not happen. Also seems to throw some exceptions.
    if is_lazy_user(request.user):
        LazyUser.objects.filter(user=request.user).delete()
        request.user.delete()
    djangologin(request, user)
    return user


def logout(request):
    djangologout(request)


def get_user_details(user):
    if user is None:
        return empty_user_details()
    if isinstance(user, AnonymousUser):
        qs = []
    else:
        # does not work with anonymous/lazy users
        qs = UserSocialAuth.objects.filter(user=user)
    details_dict = {}
    details_dict["authenticated"] = user.is_authenticated()
    details_dict["username"] = user.get_username()
    details_dict["is-lazy-user"] = is_lazy_user(user)

    if hasattr(user, 'first_name'):
        details_dict["first-name"] = user.first_name
    else:
        details_dict["first-name"] = ''

    if hasattr(user, 'last_name'):
        details_dict["last-name"] = user.last_name
    else:
        details_dict["last-name"] = ''

    if hasattr(user, 'email'):
        details_dict["email"] = user.email
    else:
        details_dict["email"] = ''

    if hasattr(user, 'is_staff'):
        details_dict["is-staff"] = user.is_staff
    else:
        details_dict["is-staff"] = False

    details_dict["providers"] = []
    for social_user in qs:
        details_dict["providers"].append(social_user.provider)
    return details_dict


def empty_user_details():
    details_dict = {}
    details_dict["authenticated"] = False
    details_dict["username"] = ''
    details_dict["is-lazy-user"] = False
    details_dict["first-name"] = ''
    details_dict["last-name"] = ''
    details_dict["email"] = ''
    details_dict["is-staff"] = False
    details_dict["providers"] = []
    return details_dict
