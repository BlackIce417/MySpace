from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import uuid
import datetime

from .forms import GalleryModelForm

from .models import *

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

@login_required(login_url="login")
def delete_gallery(request, gallery_id):
    try:
        gallery = Gallery.objects.get(id=gallery_id)
    except:
        return HttpResponse(f"Gallery not found with id {gallery_id}")
    if gallery.owner == request.user:
        gallery.delete()
        return render(request, "picture/create_new_gallery.html")
    
@login_required(login_url="login")
def gallery_manager(request, gallery_id=None):
    if gallery_id is None:
        return render(request, "picture/gallery_manager.html")
    gallery = Gallery.objects.get(id=gallery_id)
    if request.method == "POST" and request.FILES.get('upload-image'):
        try:
            images = request.FILES.getlist('upload-image')
            for image in images:
                iamge_name = datetime.datetime.now().strftime("%Y%m%d%H%M_") + str(uuid.uuid4())
                ext = image.name.split('.')[-1]
                image.name = iamge_name + "." + ext
                Picture.objects.create(gallery=gallery, image=image)
        except Exception as e:
            return HttpResponse(f"Error uploading image: {e}")
    pictures = Picture.objects.filter(gallery=gallery)
    pictures_count = pictures.count()
    context = {"gallery": gallery, "pictures": pictures, "pictures_count": pictures_count}
    return render(request, "picture/gallery_manager.html", context)
    





