from django.contrib.auth import logout
from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect

class DashboardLogoutView(View):

    def get(self, request):
        logout(request)
        messages.success(request, "Logged out successfully.")

        return redirect("DashboardLoginPage")