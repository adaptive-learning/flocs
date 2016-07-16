from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from user.services import user_service
import json


def login(request):
    if request.method != "POST":
        return HttpResponseNotAllowed('Has to be POST request.')
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    try:
        username = data['username']
    except KeyError:
        return HttpResponseBadRequest('No username given.')
    try:
        password = data['password']
    except KeyError:
        return HttpResponseBadRequest('No password given.')
    user = user_service.login(request=request,
                              username=username,
                              password=password)
    if user is None:
        return HttpResponseBadRequest(
            'Incorrect combination of username and password.')
    return HttpResponse()


def signup(request):
    if request.method != "POST":
        return HttpResponseNotAllowed('Has to be POST request.')
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    try:
        username = data['username']
        passwd = data['password']
        firstname = ''  # data.get('firstname', '')
        lastname = ''  # data.get('lastname', '')
        email = data['email']
    except KeyError:
        # field are checked in the modal on frontend
        # TODO: should not happen, but there should be better handling anyway
        return HttpResponseBadRequest('Some information is missing.')
    user = user_service.signup(request, username, firstname,
                               lastname, email, passwd)
    if not user:
        return HttpResponseBadRequest('Cannot register.')
    return HttpResponse()


def logout(request):
    if request.method != "POST":
        return HttpResponseNotAllowed('Has to be POST request.')
    user_service.logout(request)
    return HttpResponse()


def details(request):
    return JsonResponse(user_service.get_user_details(request.user))
