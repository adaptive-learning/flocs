from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseBadRequest
from lazysignup.utils import is_lazy_user
import json

from user.services import UserManager

def login(request):
    if request.method != "POST":
        return HttpResponseBadRequest('Has to be POST request.')
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    response = {}
    try:
        username = data['username']
    except KeyError:
        response['loggedIn'] = '0'
        response['msg'] = 'request doesnt contain username'
        return JsonResponse(response)
    try:
        password = data['password']
    except KeyError:
        response['loggedIn'] = '0'
        response['msg'] = 'request doesnt contain password'
        return JsonResponse(response)
    if UserManager.login(request=request, username=username, password=password):
        response['loggedIn'] = '1'
        response['username'] = username
    else:
        response['loggedIn'] = '0'
        response['msg'] = 'login failed'
    return JsonResponse(response)


def register(request):
    if request.method != "POST":
        return HttpResponseBadRequest('Has to be POST request.')
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    response = {}
    try:
        username = data['username']
        passwd = data['password']
        firstname = '' #data.get('firstname', '')
        lastname = '' #data.get('lastname', '')
        email = data['email']
    except KeyError:
        response['registred'] = '0'
        response['errorMSG'] = 'request doesnt contain one of fields'
        return JsonResponse(response)
    UserManager.register(request, username, firstname, lastname, email, passwd)


    response['registred'] = True
    return JsonResponse(response)


def logout(request):
    UserManager.logout(request)
    response = {}
    response['data'] = True
    return JsonResponse(response)


def loggedIn(request):
    response = {}
    response['username'] = UserManager.loggedIn(request)
        # TODO: refactor - not clear why loggedIn should return username, use
        # correct names and make it more explicit
    response['is-lazy-user'] = is_lazy_user(request.user)
    return JsonResponse(response)

def details(request):
    if not request.user.is_authenticated() or is_lazy_user(request.user):
        return HttpResponseBadRequest('Requires logged-in user.')
    user = UserManager.getUserInformation(request)
    details_dict = {}
    details_dict["username"] = user.username
    details_dict["email"] = user.email
    return JsonResponse(details_dict)
