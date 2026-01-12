from django.urls import path
from .views import RegistrationView, user_me

urlpatterns = [
    path("me/", user_me, name="user-me"),              # Будет доступно по /api/user/me/
    path("register/", RegistrationView.as_view(), name="user-register"), # /api/user/register/
]