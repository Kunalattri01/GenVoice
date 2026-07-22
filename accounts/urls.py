from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard-login/', DashboardLoginView.as_view(), name='DashboardLoginPage'),
    path('dashboard-logout/', DashboardLogoutView.as_view(), name='DashboardLogoutPage'),
    path('user-management/', UserManagementView.as_view(), name='UserManagementPage'),
    path('profile/', ProfileView.as_view(), name='ProfilePage'),
]