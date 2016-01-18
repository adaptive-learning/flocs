from django.test import TestCase
from .localization import LocalizationMiddleware


class LocalizationMiddlewareTestCase(TestCase):

    DEVELOPMENT_LANGUAGE_DOMAINS = {
        'cs': 'localhost:8000',
        'en': 'en.localhost:8000',
    }

    PRODUCTION_LANGUAGE_DOMAINS = {
        'cs': 'thran.cz',
        'en': 'en.thran.cz',
    }

    def setUp(self):
        self.localization_middleware = LocalizationMiddleware()

    def test_get_language_from_domain_en(self):
        language_code = self.localization_middleware.get_language_from_domain(
                'en.thran.cz', self.PRODUCTION_LANGUAGE_DOMAINS, 'ab')
        self.assertEqual(language_code, 'en')

    def test_get_language_from_domain_cs(self):
        language_code = self.localization_middleware.get_language_from_domain(
                'thran.cz', self.PRODUCTION_LANGUAGE_DOMAINS, 'ab')
        self.assertEqual(language_code, 'cs')

    def test_get_language_from_domain_localhost_en(self):
        language_code = self.localization_middleware.get_language_from_domain(
                'en.localhost:8000', self.DEVELOPMENT_LANGUAGE_DOMAINS, 'ab')
        self.assertEqual(language_code, 'en')

    def test_get_language_from_domain_localhost_cs(self):
        language_code = self.localization_middleware.get_language_from_domain(
                'localhost:8000', self.DEVELOPMENT_LANGUAGE_DOMAINS, 'ab')
        self.assertEqual(language_code, 'cs')
