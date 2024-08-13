import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse


from .forms import *
from .models import *
from topic.models import Room
from enum import Enum

# Create your views here.


def index(request):
	rooms = Room.objects.all()
	context = {"rooms": rooms}
	return render(request, 'main/index.html', context)

def user_login(request):
	page = "login"
	context = {}
	if request.method == 'POST':
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
			context['login_error'] = 'Incorrect username or password.'
			if username is not None:
				context["username"] = username
			return render(request, "main/login.html", context)
	return render(request, 'main/login.html', context)

def register(request):
	login_form = MyUserCreationForm()
	context = {"login_form": login_form}
	if request.method == 'POST':
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
	return render(request, 'main/register.html', context)


def user_logout(request):
	if request.method == "POST":
		logout(request)
		return redirect("index")
	return render(request, 'main/logout.html')

@login_required(login_url='login')
def user_center(request):
	username = request.GET.get("username")
	user = User.objects.get(username=username)
	context = {"user": user}
	return render(request, "main/user_center.html", context)

@login_required(login_url='login')
def edit_userprofile(request, opt=None):
	class EditOption(Enum):
		EDIT_USERNAME = "edit_username"
		EDIT_BIO = "edit_bio"
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
		return redirect(reverse("edit-userprofile") + "?user=" + str(request.user.id))
	try: 
		user = User.objects.get(id=request.GET.get("user"))
	except Exception as e:
		return HttpResponse(e)
	context = {"user": user}
	return render(request, "main/edit_userprofile.html", context)

