from django.shortcuts import redirect, reverse


class SuperMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path in ['/login/', '/register/'] and request.user.is_authenticated:
            return redirect(reverse('index', ))

        response = self.get_response(request)

        return response