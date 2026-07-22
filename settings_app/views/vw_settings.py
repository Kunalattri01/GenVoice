from django.views import View
from django.shortcuts import render, redirect

class SettingsView(View):

    def get(self, request):

        context = {
            'pagination' : True
        }
        return render(request, 'admin/settings/settings.html', context)
    
    def post(self, request):
        return redirect('SettingsPage')