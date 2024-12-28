from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.core.paginator import *

from . import models
from .forms import *
from .models import Question, Answer, Tag, Profile, QuestionLike
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import auth
from django.views.decorators.csrf import csrf_protect

from app.forms import LoginForm

top_users = models.Profile.objects.all()[:10]
top_tags = models.Tag.objects.all()[:10]


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


def create_content_right():
    content = {
        "tags": top_tags,
        "users": top_users,
    }

    return content


def create_content(objects, request):
    page = paginate(objects, request)
    content = create_content_right()
    content["content"] = page
    return content


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
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(reverse('profile.edit'))
            form.add_error('password', 'Invalid username or password.')
    elif request.method == 'GET':
        form = LoginForm
    return render(request, 'login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save()
            if user:
                login(request, user)
                return redirect(reverse('index'))
            else:
                return redirect(reverse('register'))
    elif request.method == 'GET':
        form = SignUpForm
    return render(request, 'signup.html', {'form': form})


def ask(request):
    popular_tags = Tag.objects.popular_tags()
    top_users = Profile.objects.top_users(5)

    return render(
        request, 'ask.html',
        context={'popular_tags': popular_tags,
                 'top_users': top_users
                 }
    )


@login_required(login_url='login', redirect_field_name='continue')
def settings(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse("settings"))
    elif request.method == 'GET':
        initial_data = model_to_dict(request.user)
        initial_data['avatar'] = request.user.profile_related.avatar
        form = ProfileEditForm(initial=initial_data)
    return render(request, 'settings.html', {'form': form})


def logout(request):
    auth.logout(request)
    return redirect(reverse('index'))
