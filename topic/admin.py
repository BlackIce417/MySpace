from django.contrib import admin
from .models import Room, AnswersRoom, CommentsRoom


# Register your models here.


class CommentsRoomAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "answer_room",
        "formatted_father_comment",
        "reply_to",
        "formatted_reply_to_comment_id",
        "comment_body",
    )

    # change CommentsRoom's display on the Django admin
    def formatted_father_comment(self, obj):
        if obj.father_comment:
            return f"{obj.father_comment.id}"
        return ""

    def formatted_reply_to_comment_id(self, obj):
        if obj.reply_to_comment_id:
            return f"{obj.reply_to_comment_id.id}"
        return ""

    # when add new comment info, this changes CommentsRoom's display on the Django admin
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        comments = CommentsRoom.objects.all()
        formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "father_comment":
            kwargs["queryset"] = comments
            formfield.label_from_instance = lambda obj: f"{obj.id}"
            return formfield
        elif db_field.name == "reply_to":
            kwargs["queryset"] = comments
            formfield.label_from_instance = lambda obj: f"{obj.username}"
            return formfield
        elif db_field.name == "reply_to_comment_id":
            kwargs["queryset"] = comments
            formfield.label_from_instance = lambda obj: f"{obj.id}"
            return formfield
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    formatted_father_comment.short_description = "father comment"


admin.site.register(Room)
admin.site.register(AnswersRoom)
admin.site.register(CommentsRoom, CommentsRoomAdmin)
