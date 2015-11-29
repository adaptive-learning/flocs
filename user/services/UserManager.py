from django.contrib.auth.models import User #this will be replaced by our class user
from django.contrib.auth import authenticate, login as log, logout as djangologout

def register(username,firstname,lastname, email, passwd):
    user = User.objects.create_user(username, email= email, password=passwd, first_name = firstname, last_name = lastname)

def login(request, username, password):
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


