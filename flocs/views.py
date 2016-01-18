"""Controllers of the flocs app
"""

from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils import translation
from django.views.decorators.csrf import ensure_csrf_cookie
import json


@ensure_csrf_cookie
def frontend_app(request):
    context = {
        'language_code': translation.get_language(),
        'language_domains': settings.LANGUAGE_DOMAINS
    }
    return render(request, 'index.html', context)


def wrong_api_call(request):
    """Serve non-existent api calls (404 error).
    """
    return HttpResponseNotFound('Wrong api call.')
