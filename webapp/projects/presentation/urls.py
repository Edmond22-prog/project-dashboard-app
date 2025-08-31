from django.urls import path

from webapp.projects.presentation.views import CreateProjectAPIView

urlpatterns = [
    path("create", CreateProjectAPIView.as_view()),
]
