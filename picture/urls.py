from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "picture"

urlpatterns = [
     path('', views.index, name='picture'),
     path('create_new_gallery', views.create_new_gallery, name='create-new-gallery'),
]
