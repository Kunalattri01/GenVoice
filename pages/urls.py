from django.urls import path
from .views import *

urlpatterns = [
    path('about/', AboutView.as_view(), name='AboutPage'),
    path('privacy_policy/', PrivacyPolicyView.as_view(), name='PrivacyPolicyPage'),
    path('terms_conditions', TermsConditionsView.as_view(), name='TermsConditionsPage'),
    path("write_for_us/", WriteForUsView.as_view(), name="WriteForUsPage"),
    path("contact/", ContactView.as_view(), name="ContactPage"),
]