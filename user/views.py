from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseBadRequest
from user.services import UserManager
import json

def login(request):
    if request.method != "POST":
        return HttpResponseBadRequest('Has to be POST request.')
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    response = {}
    try:
        username = data['username']
        password = data['password']
    except KeyError:
        response['loggedIn'] = '0'
        response['msg'] = 'request doesnt contain username or password'
        return JsonResponse(response)
    print (username,password)
    if UserManager.login(request = request, username = username, password = password):
        response['loggedIn'] = '1'
        response['username'] = username
    else:
        response['loggedIn'] = '0'
        response['msg'] = 'login failed'
    return JsonResponse(response)

def register(request):
    print (request)
    print (request.body)
    if request.method != "POST":
        return HttpResponseBadRequest('Has to be POST request.')
    print (request.POST)
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    response = {}
    try:
        username = data['username']
        passwd = data['password']
        firstname = data['firstname']
        lastname = data['lastname']
        email = data['email']
    except KeyError:
        response['registred'] = '0'
        response['msg'] = 'request doesnt contain one of fields'
        return JsonResponse(response)
    UserManager.register(username, firstname, lastname, email, passwd)
    response['registred']= '1'
    print ('user ', username, ' is created')
    return JsonResponse(response)

def logout(request):
    response = UserManager.logout(request)
    return JsonResponse(response)

def loggedIn(request):
    response = {}
    if request.user.is_authenticated():
        response['username'] = request.user.username
    else:
        response['username'] = ''
    return JsonResponse(response)
