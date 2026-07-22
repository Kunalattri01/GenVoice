from django.views import View
from django.shortcuts import render, redirect

class MessageView(View):

    def get(self, request):

        context = {}
        return render(request, 'admin/notifications/message.html', context)
    
    def post(self, request):
        return redirect('MessagePage')