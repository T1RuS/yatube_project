from django.shortcuts import render, get_object_or_404

from .models import Post, Group

OUTPUT_COUNT = 10


def index(request):
    template = 'posts/index.html'
    posts = Post.objects.order_by('-pub_date')[:OUTPUT_COUNT]
    context = {
        'posts': posts
    }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.group.all().order_by('-pub_date')[:OUTPUT_COUNT]
    template = 'posts/group_list.html'
    context = {
        'group': group,
        'posts': posts
    }
    return render(request, template, context)
