from django.urls import path

from webapp.projects.presentation.views import (
    CreateProjectAPIView,
    DashboardOverviewAPIView,
    DeleteProjectAPIView,
    EditProjectAPIView,
    RetrievePaginatedProjectsAPIView,
)

urlpatterns = [
    path("create", CreateProjectAPIView.as_view()),
    path("<str:id>/edit", EditProjectAPIView.as_view()),
    path("<str:id>/delete", DeleteProjectAPIView.as_view()),
    path("list/", RetrievePaginatedProjectsAPIView.as_view()),
    path("dashboard/", DashboardOverviewAPIView.as_view()),
]
