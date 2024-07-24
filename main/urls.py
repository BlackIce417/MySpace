from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),

	path('index/', views.index, name='index'),
	path('login/', views.user_login, name='login'),
	path('register/', views.register, name='register'),
	path('logout/', views.user_logout, name='logout'),
	path('user_center/', views.user_center, name='user-center'),
]