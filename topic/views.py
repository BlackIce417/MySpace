from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
import copy

from main.models import UserProfile, User
from .models import *


# Create your views here.


def formate_comments_info(
    answer: QuerySet[AnswersRoom],
):
    comment_info_template = {
        "answer": int,
        "comments": {
            "count": int,
            "level1": [{"comment": dict, "level2": list}],
        },
    }
    comments_info_list = []
    answer_id = [i.id for i in answer]
    for ans_id in answer_id:
        comment_info = copy.deepcopy(comment_info_template)
        comment_info["comments"]["level1"].clear()
        comment_info["answer"] = ans_id
        comment_info["comments"]["count"] = AnswersRoom.objects.get(
            id=ans_id
        ).comment_count
        comments_l1 = CommentsRoom.objects.filter(answer_room_id=ans_id, level=1)
        if comments_l1.exists():
            for l1 in comments_l1:
                comments_l2 = CommentsRoom.objects.filter(
                    answer_room_id=ans_id, level=2, father_comment_id=l1.id
                )
                if comments_l2.exists():
                    comment_info["comments"]["level1"].append(
                        {"comment": l1, "level2": comments_l2}
                    )
                else:
                    comment_info["comments"]["level1"].append(
                        {"comment": l1, "level2": CommentsRoom.objects.none()}
                    )
        else:
            comment_info["comments"]["level1"] = []
        comments_info_list.append(comment_info)
    print(comments_info_list)
    return comments_info_list


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
    comments_info = formate_comments_info(answers,)
    context = {
        "topic": topic,
        "user_profile": user_profile,
        "answers": answers,
        "comments": comments_info,
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
def reply_to(request, comment_id, father_comment_id=None):
    if request.method == "GET":
        try:
            comment = CommentsRoom.objects.get(id=comment_id)
            user = comment.user
        except:
            user = None
            comment = None
        context = {
            "user": user,
            "comment": comment,
            "father_comment_id": father_comment_id,
        }
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
        if father_comment_id is None:
            comment = CommentsRoom.objects.create(
                user=request.user,
                comment_body=text,
                answer_room=answer_room,
                reply_to=comment.user,
                reply_to_comment_id=comment,
                father_comment_id=comment_id,
                level=2,
            )
        else:
            comment = CommentsRoom.objects.create(
                user=request.user,
                comment_body=text,
                answer_room=answer_room,
                reply_to=comment.user,
                reply_to_comment_id=comment,
                father_comment_id=father_comment_id,
                level=2,
            )
        comment.save()
        messages.success(request, "Reply Success")
        return redirect(
            reverse("topic") + "?topic_id=" + str(answer_room.topic_room.id)
        )
