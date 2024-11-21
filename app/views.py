from django.shortcuts import render
from django.core.paginator import *

from .models import Question, Answer, Tag, Profile, QuestionLike


def paginate(objects_list, request, per_page):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(objects_list, per_page)

    try:
        page_num = int(page_num)
    except ValueError:
        page_num = 1

    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page


def index(request):
    questions = Question.objects.all().order_by('-created_at')
    popular_tags = Tag.objects.popular_tags()
    top_users = Profile.objects.top_users(5)

    page = paginate(questions, request, 5)
    return render(
        request, 'index.html',
        context={'questions': page.object_list,
                 'page_obj': page,
                 'popular_tags': popular_tags,
                 'top_users': top_users
                 }
    )


def hot(request):
    hot_questions = Question.objects.best_questions()
    popular_tags = Tag.objects.popular_tags()
    top_users = Profile.objects.top_users(5)

    page = paginate(hot_questions, request, 5)
    return render(
        request, 'hot.html',
        context={'questions': page.object_list,
                 'page_obj': page,
                 'popular_tags': popular_tags,
                 'top_users': top_users
                 }
    )


def tag(request, tag_name):
    popular_tags = Tag.objects.popular_tags()
    questions = Question.objects.get_questions_by_tag_name(tag_name)

    top_users = Profile.objects.top_users(5)

    page = paginate(questions, request, 5)
    return render(
        request,
        template_name="tag.html",
        context={
            'questions': page.object_list,
            'page_obj': page,
            'tag_name': tag_name,
            'popular_tags': popular_tags,
            'top_users': top_users
        }
    )


def question(request, question_id):
    popular_tags = Tag.objects.popular_tags()
    top_users = Profile.objects.top_users(5)
    answers = Answer.objects.get_answers_by_question_id(question_id)
    likes = QuestionLike.objects.all()

    page = paginate(answers, request, 5)

    return render(
        request, 'one_question.html',
        context={'question': Question.objects.get_question_by_id(question_id),
                 'page_obj': page,
                 'answers': page.object_list,
                 'popular_tags': popular_tags,
                 'top_users': top_users,
                 'likes': likes
                 })


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def ask(request):
    popular_tags = Tag.objects.popular_tags()
    top_users = Profile.objects.top_users(5)

    return render(
        request, 'ask.html',
        context={'popular_tags': popular_tags,
                 'top_users': top_users
                 }
        )


def settings(request):
    return render(request, 'settings.html')
