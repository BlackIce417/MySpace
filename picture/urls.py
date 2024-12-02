from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "picture"

urlpatterns = [
     path('', views.index, name='picture'),
     path('gallery_manager/', views.gallery_manager, name='create-new-gallery'),
     path('delete_gallery/<int:gallery_id>', views.delete_gallery, name='delete-gallery'),
     path('gallery_manager/<int:gallery_id>', views.gallery_manager, name='add-picture'),
]
