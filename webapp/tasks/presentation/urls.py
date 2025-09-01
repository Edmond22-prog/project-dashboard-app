from django.urls import path

from webapp.tasks.presentation.views import CreateTaskAPIView


urlpatterns = [
    path("create", CreateTaskAPIView.as_view()),
]

