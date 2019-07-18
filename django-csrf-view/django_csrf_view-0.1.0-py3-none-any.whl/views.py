from django.http.response import JsonResponse
from django.middleware.csrf import get_token
from django.views import View


class CSRFView(View):
    def get(self, request, **kwargs):
        token = get_token(request)
        response = JsonResponse({
            'token': token,
        })

        return response
