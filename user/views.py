from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseBadRequest
from user.services import UserManager

def login(request):
    if request.method != "POST":
        return HttpResponseBadRequest('Has to be POST request.')
    user = request.POST['username']
    passwd = request.POST['password']
    response = UserManager.login(user, passwd)
    return JsonResponse(response)

def register(request):
    if request.method != "POST":
        return HttpResponseBadRequest('Has to be POST request.')
    username = request.POST['username']
    passwd = request.POST['password']
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    email = request.POST['email']
    response = UserManager.register(username, firstname, lastname, email, passwd)
    response = JsonResponse(response)

def logout(request):
    response = UserManager.logout(request)
    return response
