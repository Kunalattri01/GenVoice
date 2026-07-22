from django.urls import path
from .views import *

urlpatterns = [
    path('', ListArticlesView.as_view() ,name='ListArticlesPage'),
    path('manage-articles/', ManageArticlesView.as_view() ,name='ManageArticlesPage'),
]