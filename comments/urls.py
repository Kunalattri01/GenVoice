from django.urls import path
from .views import *

urlpatterns = [
    path('', CommentsView.as_view() ,name='CommentsPage')
]