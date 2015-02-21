import settings

class FinetoothEnvironmentMiddleware:
    def process_request(self, request):
        request.possible_environments = settings.Environment
        request.environment = settings.ENVIRONMENT
