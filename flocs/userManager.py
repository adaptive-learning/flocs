from django.contrib.auth.models import User #this will be replaced by our class user
from django.contrib.auth import authenticate, login, logout

def createUser(username,firstname,lastname, email, passwd):
    user = User.objects.create_user(username, email= email, password=passwd)
    user.first_name = firstname
    user.last_name = lastname
    user.save()

def login(request):
    username = request.POST['username']
    passwd = request.POST['password']
    user = authenticate(username, passwd)
    if user is not None:
        login(request, user)
        return 1
    else:
        return 0

def logout(request):
    logout(request)


