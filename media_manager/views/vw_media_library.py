from django.views import View
from django.shortcuts import render, redirect

class MediaLibraryView(View):

    def get(self, request):

        context = {
            'pagination' : True,
        }
        return render(request, 'admin/media/media_library.html', context)
    
    def post(self, request):
        return redirect('MediaLibraryPage')