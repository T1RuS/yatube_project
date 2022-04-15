from django.shortcuts import render, get_object_or_404

from .models import Post, Group, User

OUTPUT_COUNT = 10


def index(request):
    template = 'posts/index.html'
    posts = Post.objects.all()[:OUTPUT_COUNT]
    print(type(posts))
    context = {
        'posts': posts
    }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:OUTPUT_COUNT]
    template = 'posts/group_list.html'
    context = {
        'group': group,
        'posts': posts
    }
    return render(request, template, context)


def user_posts(request, slug):
    template = 'posts/group_list.html'
    user = get_object_or_404(User, username=slug)
    posts = user.posts.all()[:OUTPUT_COUNT]
    context = {
        'posts': posts
    }
    return render(request, template, context)
