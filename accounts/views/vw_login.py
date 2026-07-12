from django.views import View
from django.shortcuts import render, redirect

class DashboardLoginView(View):

    def get(self, request):

        context = {}

        return render(request, 'admin/auth/login.html', context)
    


    def post(self, request):

        return redirect('')