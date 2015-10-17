"""Controllers of the flocs app
"""

from django.http import HttpResponseNotFound


def wrong_api_call(request):
    """Serve non-existent api calls (404 error).
    """
    return HttpResponseNotFound('Wrong api call.')
