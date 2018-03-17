import settings

from django.utils import deprecation

from django.core.handlers.wsgi import WSGIRequest


class FinetoothEnvironmentMiddleware(deprecation.MiddlewareMixin):
    def process_request(self, request: WSGIRequest) -> None:
        request.possible_environments = settings.Environment
        request.environment = settings.ENVIRONMENT
