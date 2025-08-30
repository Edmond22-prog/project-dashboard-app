from django.urls import path

from webapp.users.presentation.views import RegisterUserAPIView


urlpatterns = [
    path("register", RegisterUserAPIView.as_view()),
]
