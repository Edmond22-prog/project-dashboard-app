from django.urls import path

from webapp.tasks.presentation.views import (
    CreateTaskAPIView,
    EditTaskAPIView,
    RetrievePaginatedTasksAPIView,
    StartTaskTimerAPIView,
    StopTaskTimerAPIView,
)

urlpatterns = [
    path("create", CreateTaskAPIView.as_view()),
    path("list/", RetrievePaginatedTasksAPIView.as_view()),
    path("<str:id>/edit", EditTaskAPIView.as_view()),
    path("start-timer", StartTaskTimerAPIView.as_view()),
    path("stop-timer", StopTaskTimerAPIView.as_view()),
]
