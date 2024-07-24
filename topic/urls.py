from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.topic_room, name='topic'),
	path('answer/', views.answer_question, name='answer'),
	path('delete-answer/<int:answer_id>/', views.delete_answer, name='delete_answer'),
	path('quick-add-comment/<int:answer_id>', views.quick_add_comment, name='quick_add_comment'),
	path('delete-comment/<int:comment_id>', views.delete_comment, name='delete_comment'),
	path('comment-reply/<int:comment_id>', views.reply_to, name='reply_comment'),
	path('comment-reply/<int:father_comment_id>/<int:comment_id>', views.reply_to, name='reply_under_father_comment'),
]
