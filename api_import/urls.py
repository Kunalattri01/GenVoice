from django.urls import path
from .views import *

urlpatterns = [
    path('', APIImportView.as_view(), name='APIImportPage'),
]