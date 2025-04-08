# api/urls.py
from django.urls import path
from .views import JobListView, JobSemanticSearchView, JobDetailView

urlpatterns = [
    path('jobs/', JobListView.as_view(), name='job-list'),
    path('jobs/<int:job_id>/', JobDetailView.as_view(), name='job-detail'),
    path('search/', JobSemanticSearchView.as_view(), name='job-search'),
]
