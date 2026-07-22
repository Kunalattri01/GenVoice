from django.urls import path
from .views import *

urlpatterns = [
    path('categories/', CategoriesView.as_view() ,name='CategoriesPage'),
    path('tags/', TagsView.as_view() ,name='TagsPage'),
    path('authors/', AuthorsView.as_view() ,name='AuthorsPage'),
    path('sources/', SourcesView.as_view() ,name='SourcesPage'),
]