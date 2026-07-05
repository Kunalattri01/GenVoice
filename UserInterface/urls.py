from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='HomePage'),
    path("news/<str:encoded_uri>/", NewsDetailView.as_view(), name="news_detail"),
]
