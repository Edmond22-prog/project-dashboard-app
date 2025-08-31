from django.urls import path

from webapp.projects.presentation.views import CreateProjectAPIView, EditProjectAPIView

urlpatterns = [
    path("create", CreateProjectAPIView.as_view()),
    path("<str:id>/edit", EditProjectAPIView.as_view()),
]
