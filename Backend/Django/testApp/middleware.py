# middleware.py
from django.http import JsonResponse
from .models import Token

class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.headers.get('Authorization')
        if token:
            try:
                token = Token.objects.get(token=token)
                request.user = token.user
            except Token.DoesNotExist:
                return JsonResponse({'error': 'Invalid token'}, status=401)
        else:
            request.user = None
        return self.get_response(request)
