from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages

from main.models import UserProfile, User
from .models import *


# Create your views here.
def topic_room(request):
    if request.method == "POST":
        return redirect("topic")
    topic_id = (
        request.GET.get("topic_id") if request.GET.get("topic_id") is not None else ""
    )
    topic = Room.objects.get(id=topic_id)
    try:
        user_profile = UserProfile.objects.get(user=topic.owner)
    except:
        user_profile = None
    answers = AnswersRoom.objects.filter(topic_room=topic)
    comments = CommentsRoom.objects.filter(answer_room__in=answers)
    ans_flag = True
    for ans in answers:
        if ans.owner == request.user:
            ans_flag = False
            break
    context = {
        "topic": topic,
        "user_profile": user_profile,
        "answers": answers,
        "comments": comments,
        "ans_flag": ans_flag,
    }
    return render(request, "topic/topic.html", context)


@login_required(login_url="login")
def answer_question(request):
    topic_id = request.GET.get("topic_id")
    if topic_id is None:
        topic_id = request.POST.get("topic_id")
    topic = Room.objects.get(id=topic_id)
    if request.method == "GET":
        try:
            user_profile = UserProfile.objects.get(user=topic.owner)
        except:
            user_profile = None
        try:
            answer_context = AnswersRoom.objects.get(
                owner=request.user, topic_room=topic
            ).answer_body
        except:
            answer_context = None
        context = {
            "user_profile": user_profile,
            "topic": topic,
            "answer_context": answer_context,
        }
        return render(request, "topic/answer.html", context)
    else:
        ans_body = request.POST.get("answer_body")
        user = request.user
        # if answer already exists, then update it
        try:
            ansobj = AnswersRoom.objects.get(topic_room=topic, owner=user)
            ansobj.answer_body = ans_body
            ansobj.save()
        except:
            form = AnswersRoom(owner=user, answer_body=ans_body, topic_room=topic)
            form.save()
        return redirect("/topic/?topic_id=" + str(topic_id))


def delete_answer(request, answer_id):
    if request.method == "POST":
        answer = AnswersRoom.objects.get(id=answer_id)
        answer.delete()
        return redirect(reverse("topic") + "?topic_id=" + str(answer.topic_room.id))


@login_required(login_url="login")
def quick_add_comment(request, answer_id):
    if request.method == "POST":
        try:
            print(answer_id)
            answer = AnswersRoom.objects.get(id=answer_id)

            comment = CommentsRoom.objects.create(
                user=request.user,
                answer_room=answer,
                comment_body=request.POST.get("comment"),
            )
            comment.save()

            return redirect(reverse("topic") + "?topic_id=" + str(answer.topic_room.id))
        except Exception as e:
            return HttpResponse(f"Error: {e}")


@login_required(login_url="login")
def delete_comment(request, comment_id):
    try:
        comment = CommentsRoom.objects.get(id=comment_id)
        comment.delete()
        return redirect(
            reverse("topic") + "?topic_id=" + str(comment.answer_room.topic_room.id)
        )
    except Exception as e:
        return HttpResponse(f"{e}")


@login_required(login_url="login")
def reply_to(request, comment_id):
    if request.method == "GET":
        try:
            comment = CommentsRoom.objects.get(id=comment_id)
            user = comment.user
        except:
            user = None
            comment = None
        context = {"user": user, "comment": comment}
        return render(
            request,
            "topic/add_comment.html",
            context,
        )
    elif request.method == "POST":
        text = request.POST.get("answer_body")
        try:
            comment = CommentsRoom.objects.get(id=comment_id)
            answer_room = comment.answer_room
        except Exception as e:
            return HttpResponse(f"Error: {e}")
        comment = CommentsRoom.objects.create(
            user=request.user,
            comment_body=text,
            answer_room=answer_room,
            reply_to=comment.user,
            reply_to_comment_id=comment,
            father_comment_id=comment_id,
        )
        comment.save()
        messages.success(request, "Reply Success")
        return redirect(
            reverse("topic") + "?topic_id=" + str(answer_room.topic_room.id)
        )
