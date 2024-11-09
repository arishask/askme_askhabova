import copy

from django.shortcuts import render
from django.core.paginator import Paginator

QUESTIONS = [
    {
        'title': f'Title {i}',
        'id': i,
        'text': f'This is text for question #{i}'
    } for i in range(30)
]


def paginate(objects_list, request, per_page=5):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(QUESTIONS, per_page)
    page = paginator.page(page_num)
    return page


def index(request):
    return render(
        request, 'index.html',
        context={'questions': paginate(QUESTIONS, request, 5),
                 'page_obj': paginate(QUESTIONS, request, 5)})


def hot(request):
    return render(
        request, 'hot.html',
        context={'questions': paginate(QUESTIONS.reverse(), request, 5),
                 'page_obj': paginate(QUESTIONS.reverse(), request, 5)})


def tag(request):
    return render(
        request, 'tag.html',
        context={'questions': paginate(QUESTIONS, request, 3),
                 'page_obj': paginate(QUESTIONS, request, 3)})


def question(request, question_id):
    one_question = QUESTIONS[question_id]
    return render(
        request, 'one_question.html',
        context={'questions': paginate(QUESTIONS[question_id], request, 2),
                 'page_obj': paginate(QUESTIONS[question_id], request, 2)})


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def ask(request):
    return render(request, 'ask.html')


def settings(request):
    return render(request, 'settings.html')
