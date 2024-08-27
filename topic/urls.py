from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'topic'

urlpatterns = [
	path('', views.topic_room, name='topic'),
	path('answer/', views.answer_question, name='answer'),
	path('delete-answer/<int:answer_id>/', views.delete_answer, name='delete_answer'),
	path('quick-add-comment/<int:answer_id>', views.quick_add_comment, name='quick_add_comment'),
	path('delete-comment/<int:comment_id>', views.delete_comment, name='delete_comment'),
	path('comment-reply/<int:comment_id>', views.reply_to, name='reply_comment'),
	path('comment-reply/<int:father_comment_id>/<int:comment_id>', views.reply_to, name='reply_under_father_comment'),
    path('follow-topic/<int:topic_id>', views.follow_topic, name='follow_topic'),
    path('unfollow-topic/<int:topic_id>', views.unfollow_topic, name='unfollow_topic'),
    path('approve-answer/<int:answer_id>/<str:approve_status>', views.approve_answer, name='approve_answer'),
]
