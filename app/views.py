from django.shortcuts import render
from django.core.paginator import *

QUESTIONS = [
    {
        'title': f'Title {i}',
        'id': i,
        'text': f'This is text for question #{i}'
    } for i in range(30)
]

ANSWERS = [
    {
        'title': f'Title {i}',
        'id': i,
        'text': f'This is answer for question #{i}'
    } for i in range(4)
]


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
    return render(
        request, 'index.html',
        context={'questions': paginate(QUESTIONS, request, 5)})


def hot(request):
    hot_questions = QUESTIONS.copy()
    hot_questions.reverse()
    return render(
        request, 'hot.html',
        context={'questions': paginate(hot_questions, request, 5)})


def tag(request):
    return render(
        request, 'tag.html',
        context={'questions': paginate(QUESTIONS, request, 3)})


def question(request, question_id):
    one_question = QUESTIONS[question_id]
    return render(
        request, 'one_question.html',
        context={'answers': paginate(ANSWERS, request, 2),
                 'question': one_question})


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def ask(request):
    return render(request, 'ask.html')


def settings(request):
    return render(request, 'settings.html')
