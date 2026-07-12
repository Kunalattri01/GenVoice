from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', DashboardLoginView.as_view(), name='DashboardLoginPage'),
]