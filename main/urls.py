from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),

	path('index/', views.index, name='index'),
	path('login/', views.user_login, name='login'),
	path('register/', views.register, name='register'),
	path('logout/', views.user_logout, name='logout'),
	path('user_center/', views.user_center, name='user-center'),
    path('user_center/<str:opt>', views.user_center, name='user-center-opt'),
    path('edit_userprofile/', views.edit_userprofile, name='edit-userprofile'),
	path('edit_userprofile/<str:opt>/', views.edit_userprofile, name='edit-userprofile-opt'),
]