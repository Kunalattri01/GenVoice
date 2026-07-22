from django.views import View
from django.shortcuts import render, redirect

class CommentsView(View):

    def get(self, request):

        context = {}
        return render(request, 'admin/comments/comments.html', context)
    
    def post(self, request):
        return redirect('CommentsPage')