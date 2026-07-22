from django.views import View
from django.shortcuts import render, redirect

class APIImportView(View):

    def get(self, request):

        context = {}
        return render(request, 'admin/api/api_imports.html', context)

    def post(self, request):
        return redirect('APIImportPage')    