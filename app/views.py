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


def index(request):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(QUESTIONS, 5)
    page = paginator.page(page_num)
    return render(
        request, 'index.html',
        context={'questions': page.object_list, 'page_obj': page})


def hot(request):
    hot_questions = copy.deepcopy(QUESTIONS)
    hot_questions.reverse()
    return render(request, 'hot.html', context={'questions': hot_questions})


def tag(request):
    return render(request, 'tag.html')


def question(request, question_id):
    one_question = QUESTIONS[question_id]
    return render(request, 'one_question.html', context={'question': one_question})


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def ask(request):
    return render(request, 'ask.html')


def settings(request):
    return render(request, 'settings.html')
