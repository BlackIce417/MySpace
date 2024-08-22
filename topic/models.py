from django.db import models
from main.models import User

# Create your models here.


class Room(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(max_length=500)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name="rooms")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class AnswersRoom(models.Model):
    topic_room = models.ForeignKey(Room, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    answer_body = models.TextField(max_length=2000)
    comment_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.owner.username} - {self.topic_room}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.owner not in self.topic_room.participants.all():
            self.topic_room.participants.add(self.owner)

    class Meta:
        ordering = ["-created_at", "-updated_at"]


class CommentsRoom(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment_host"
    )
    answer_room = models.ForeignKey(AnswersRoom, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comment_receiver",
        null=True,
        blank=True,
    )
    reply_to_comment_id = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="reply_to_comment",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    comment_body = models.TextField(max_length=2000)
    father_comment = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="father comment",
    )
    level = models.IntegerField(default=1, choices=[(1, 'Level 1'), (2, 'Level 2'),], null=False, blank=False)

    def __str__(self):
        return f"{self.answer_room} - {self.user}"

    class Meta:
        ordering = ["-created_at"]


class TopicFollow(models.Model):
    user = models.ForeignKey("main.UserProfile", on_delete=models.CASCADE)
    topic_room = models.ForeignKey(Room, on_delete=models.CASCADE)
    follow_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.room}"
    
    class Meta:
        unique_together = ('user', 'topic_room')
        ordering = ["-follow_at"]
