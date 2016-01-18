from django.conf import settings
from django.utils import translation


class LocalizationMiddleware(object):

    def process_request(self, request):
        http_host = request.META['HTTP_HOST']
        language_code = self.get_language_from_domain(http_host,
                settings.LANGUAGE_DOMAINS, settings.LANGUAGE_CODE)
        translation.activate(language_code)

    def get_language_from_domain(self, http_host, language_domains, fallback):
        domain = http_host.split(':')[0]
        for language_code, language_domain in language_domains.items():
            if language_domain.startswith(domain):
                return language_code
        return fallback
