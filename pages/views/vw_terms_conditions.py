from django.shortcuts import render
from django.views import View

class TermsConditionsView(View):
    
    def get(self, request):
        return render(request, 'pages/terms_conditions.html')