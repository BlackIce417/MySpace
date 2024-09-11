from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import GalleryModelForm

# Create your views here.


def index(request):
    return render(request, "picture/picture.html")

@login_required(login_url="login")
def create_new_gallery(request):
    if request.method == "POST":
        # gallery_name = request.POST.get("gallery-name")
        # gallery_description = request.POST.get("gallery-description")
        print(request.POST)
        form = GalleryModelForm(request.POST)
        if form.is_valid():
            gallery = form.save(commit=False)
            gallery.owner = request.user
            gallery.save()
            return HttpResponse("Gallery created successfully")
        else: 
            print(form.errors)
            return HttpResponse("Error creating gallery")
    return render(request, "picture/create_new_gallery.html")
