from django.conf import settings
from django.utils import translation
import re


class LocalizationMiddleware(object):

    def process_request(self, request):
        http_host = request.META['HTTP_HOST']
        language_code = self.get_language_from_domain(http_host)
        #print('LocalizationMiddleware:', language_code)
        translation.activate(language_code)

    def get_language_from_domain(self, http_host):
        for language_code, domain_pattern in settings.LANGUAGE_DOMAINS:
            if re.search(domain_pattern, http_host):
                return language_code
        return settings.LANGUAGE_CODE
