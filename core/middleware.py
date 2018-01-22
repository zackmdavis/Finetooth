import settings

from django.utils import deprecation

class FinetoothEnvironmentMiddleware(deprecation.MiddlewareMixin):
    def process_request(self, request):
        request.possible_environments = settings.Environment
        request.environment = settings.ENVIRONMENT
