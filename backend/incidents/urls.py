from django.urls import path

from . import views

app_name = 'incidents'

urlpatterns = [
    path('incidents/', views.IncidentListCreateView.as_view(), name='incident-list'),
    path('incidents/<int:pk>/', views.IncidentDetailView.as_view(), name='incident-detail'),
    path('incidents/<int:pk>/status/', views.IncidentStatusView.as_view(), name='incident-status'),
    path('incidents/<int:pk>/history/', views.IncidentHistoryView.as_view(), name='incident-history'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]
