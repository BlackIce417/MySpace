import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.urls import reverse
from django.db.models import QuerySet
from django.db.models import Count
from django.core.files.storage import FileSystemStorage


from .forms import *
from .models import *
from topic.models import Room, AnswersRoom
from picture.models import Gallery, Picture
from enum import Enum
import hashlib


# Create your views here.


def index(request):
    rooms = Room.objects.all()
    context = {"rooms": rooms}
    return render(request, "main/index.html", context)


def user_login(request):
    page = "login"
    context = {}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Incorrect username or password.")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            context["login_error"] = "Incorrect username or password."
            if username is not None:
                context["username"] = username
            return render(request, "main/login.html", context)
    return render(request, "main/login.html", context)


def register(request):
    login_form = MyUserCreationForm()
    context = {"login_form": login_form}
    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password1 == password2:
            form = MyUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect("index")
            else:
                error_info = json.loads(form.errors.as_json())
                # print(error_info)
                # register_errors = error_info["register_errors"]
                context["register_error"] = error_info
                return render(request, "main/register.html", context)
    return render(request, "main/register.html", context)


def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect("index")
    return render(request, "main/logout.html")


def get_topic_followed_count(topic: Room, user: User) -> int:
    user_count = TopicFollow.objects.filter(topic_room=topic).aggregate(count=Count('user'))['count']
    return user_count


def format_topic_info(topics: QuerySet, user: User) -> list:
    # topics_template = [{"topic": Room, "followed_count": int}]
    formatted_topics = []
    for topic in topics:
        followed_count = get_topic_followed_count(topic, user)
        formatted_topics.append({"topic": topic, "followed_count": followed_count})
    return formatted_topics


def user_center(request, opt="all"):
    username = request.GET.get("username")
    try:
        user = User.objects.get(username=username)
    except:
        return HttpResponse("User not found.")
    context = {"user": user, "opt": opt}
    if opt == "all" or opt == "topic":
        try:
            answers = AnswersRoom.objects.filter(owner=user)
            topics = Room.objects.filter(owner=user)
            formatted_topics = format_topic_info(topics, user)
        except Exception as e:
            return HttpResponse(f"Error: {e}")
        context["topics"] = formatted_topics
    elif opt == "answer":
        try:
            answers = AnswersRoom.objects.filter(owner=user)
        except Exception as e:
            return HttpResponse(f"Error: {e}")
        context["answers"] = answers
    elif opt == "gallery":
        try: 
            galleries = Gallery.objects.filter(owner=user)
        except Exception as e:
            return HttpResponse(f"Error: {e}")
        gallery_info = []
        for gallery in galleries:
            try:
                pictures = Picture.objects.filter(gallery=gallery)
                pictures_count = pictures.count()
            except:
                pictures = []
                pictures_count = 0
            gallery_info.append({"gallery": gallery, "pictures": pictures, "pictures_count": pictures_count})
        print(gallery_info)
        context["gallery"] = gallery_info
    return render(request, "main/user_center.html", context) 

@login_required(login_url="login")
def edit_userprofile(request, opt=None):
    class EditOption(Enum):
        EDIT_USERNAME = "edit_username"
        EDIT_BIO = "edit_bio"
        EDIT_AVATAR = "edit_avatar"

    if request.method == "POST":
        try:
            edit_option = EditOption(opt)
        except ValueError as e:
            return HttpResponse(f"{e}")
        user = User.objects.get(id=request.user.id)
        if edit_option == EditOption.EDIT_USERNAME:
            username = request.POST.get("username")
            user.username = username
            user.save()
        elif edit_option == EditOption.EDIT_BIO:
            bio = request.POST.get("bio")
            user.userprofile.bio = bio
            user.userprofile.save()
        elif edit_option == EditOption.EDIT_AVATAR:
            avatar = request.FILES["user-avatar"]
            if avatar:
                fs = FileSystemStorage(location="media/main/images/avatars")

                md5 = hashlib.md5()
                for chunk in avatar.chunks():
                    md5.update(chunk)
                md5_hash = md5.hexdigest().upper()

                ext = avatar.name.split('.')[-1]
                unique_filename = f"IMG_{md5_hash}.{ext}"
                filename = fs.save(unique_filename, avatar)
                # old_avatar = user.userprofile.avatar.url
                # fs.delete(old_avatar.split("/")[-1])
                user.userprofile.avatar = f"/main/images/avatars/{filename}"
                user.userprofile.save()
        return redirect(reverse("edit-userprofile") + "?user=" + str(request.user.id))
    try:
        user = User.objects.get(id=request.GET.get("user"))
    except Exception as e:
        return HttpResponse(e)
    context = {"user": user}
    return render(request, "main/edit_userprofile.html", context)
