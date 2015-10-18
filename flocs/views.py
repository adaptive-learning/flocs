"""Controllers of the flocs app
"""

from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.shortcuts import render_to_response
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def frontend_app(request):
    return render_to_response('index.html')


def wrong_api_call(request):
    """Serve non-existent api calls (404 error).
    """
    return HttpResponseNotFound('Wrong api call.')
