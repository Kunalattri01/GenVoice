from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from accounts.models import User

class DashboardLoginView(View):

    def get(self, request):

        if request.user.is_authenticated:
            return redirect("DashboardPage")

        context = {}
        return render(request, 'admin/auth/login.html', context)

    def post(self, request):

        email = request.POST.get("email")
        password = request.POST.get("password")
        remember = request.POST.get("remember")

        if not email or not password:
            print('nothing provided')
            messages.error(request, "Please enter email and password.")
            return redirect("DashboardLoginPage")
        
        user_obj = User.objects.filter(email=email).first()

        if not user_obj:
            print('Invalid Credentials')
            messages.error(request, "Invalid email or password.")
            return redirect("DashboardLoginPage")

        user = authenticate(request, username = user_obj.username, password = password)

        if user is not None:

            if not user.is_active:
                print('Account Disabled')
                messages.error(request, "Your account has been disabled.")
                return redirect("DashboardLoginPage")

            login(request, user)

            if not remember:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(60 * 60 * 24 * 30)

            name = user.first_name if user.first_name else user.username
            messages.success(request, f"Welcome back, {name}!")

            return redirect("DashboardPage")

        messages.error(request, "Invalid email or password.")

        return redirect("DashboardLoginPage")