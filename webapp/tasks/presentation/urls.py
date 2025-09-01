from django.urls import path

from webapp.tasks.presentation.views import (
    CreateTaskAPIView,
    RetrievePaginatedTasksAPIView,
)

urlpatterns = [
    path("create", CreateTaskAPIView.as_view()),
    path("list/", RetrievePaginatedTasksAPIView.as_view()),
]
