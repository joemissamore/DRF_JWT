from rest_framework_simplejwt.state import token_backend


class CustomUserMiddleware:
    def __init__(self, get_response):
        # One-time configuration and initialization.
        # Called when the server first starts.
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        AUTH_HEADER = request.META.get('HTTP_AUTHORIZATION', None)
        token = AUTH_HEADER.split(" ")[1]
        decoded_token = token_backend.decode(token, verify=False)

        company = decoded_token['custom_field']
        request.custom_field = company
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        return response
