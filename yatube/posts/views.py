from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    templates = 'posts/index.html'
    context = {
        'title': "Это главная страница проекта Yatube"
    }
    return render(request, templates, context)


def group_posts(request, pk):
    templates = 'posts/group_list.html'
    context = {
        'title': "Здесь будет информация о группах проекта Yatube"
    }
    return render(request, templates)
