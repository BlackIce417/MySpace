from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *


@receiver(post_save, sender=CommentsRoom)
def update_comment_count_on_save(sender, instance, **kwargs):
	answer_room = instance.answer_room
	answer_room.comment_count = CommentsRoom.objects.filter(answer_room=answer_room).count()
	answer_room.save(update_fields=['comment_count'])


@receiver(post_delete, sender=CommentsRoom)
def update_comment_count_on_delete(sender, instance, **kwargs):
	answer_room = instance.answer_room
	answer_room.comment_count = CommentsRoom.objects.filter(answer_room=answer_room).count()
	answer_room.save()
