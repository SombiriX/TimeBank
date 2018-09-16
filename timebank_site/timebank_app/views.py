from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response


class AppView(TemplateView):

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return render(request, 'index.html', context=None)


@api_view(['GET'])
def current_user(request):
    user = request.user
    user_prefs = {
        "complete_anim": getattr(user, 'complete_anim', None),
        "twentyFourClock": getattr(user, 'twentyFourClock', None),
    }
    return Response({
        "username": getattr(user, 'username', None),
        "first_name": getattr(user, 'first_name', None),
        "last_name": getattr(user, 'last_name', None),
        "email": getattr(user, 'email', None),
        "last_login": getattr(user, 'last_login', None),
        "date_joined": getattr(user, 'date_joined', None),
        "user_prefs": user_prefs,
    })
