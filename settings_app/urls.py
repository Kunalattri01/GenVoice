from django.urls import path
from .views import *

urlpatterns = [
    path('', SettingsView.as_view(), name='SettingsPage'),
]