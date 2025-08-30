from django.urls import path

from webapp.users.presentation.views import LoginAPIView, RegisterUserAPIView

urlpatterns = [
    path("register", RegisterUserAPIView.as_view()),
    path("login", LoginAPIView.as_view()),
]
