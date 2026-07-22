from django.views import View
from django.shortcuts import render, redirect

class NotificationView(View):

    def get(self, request):

        context = {}
        return render(request, 'admin/notifications/notification.html', context)
    
    def post(self, request):
        return redirect('NotificationPage')