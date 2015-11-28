import logging

class LoggingUtils(object):
    def __init__(self):
        self.logger = logging.getLogger('django.request')
        self.debug  = logging.getLogger('django.request').isEnabledFor(logging.DEBUG)

    def log_request(self, request):
        if self.debug:
            body = request.body
        else:
            body = ''

        self.logger.info('%s %s %s', request.method, request.path_info, body)
        return None

