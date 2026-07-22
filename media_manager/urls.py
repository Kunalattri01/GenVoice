from django.urls import path
from .views import *

urlpatterns = [
    path('', MediaLibraryView.as_view() ,name='MediaLibraryPage'),
]