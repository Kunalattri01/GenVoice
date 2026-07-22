from django.urls import path
from .views import *

urlpatterns = [
    path('notification/', NotificationView.as_view(), name='NotificationPage'),
    path('message/', MessageView.as_view(), name='MessagePage'),
]