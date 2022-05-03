from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import Post, Group, User

OUTPUT_COUNT = 10


def index(request):
    template = 'posts/index.html'

    post_list = Post.objects.all()
    paginator = Paginator(post_list, OUTPUT_COUNT)

    if request.GET.get('page'):
        page_number = request.GET.get('page')
    else:
        page_number = 1

    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)

    post_list = Post.objects.all()
    paginator = Paginator(post_list, OUTPUT_COUNT)

    if request.GET.get('page'):
        page_number = request.GET.get('page')
    else:
        page_number = 1

    page_obj = paginator.get_page(page_number)

    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    user = get_object_or_404(User, username=username)
    post_list = user.posts.all()[:OUTPUT_COUNT]
    paginator = Paginator(post_list, OUTPUT_COUNT)

    if request.GET.get('page'):
        page_number = request.GET.get('page')
    else:
        page_number = 1

    page_obj = paginator.get_page(page_number)
    count_posts = len(user.posts.all())

    context = {
        'page_obj': page_obj,
        'username': user.get_full_name(),
        'count_posts': count_posts,
    }
    return render(request, template, context)


def post_detail(request, post_id):

    post = Post.objects.get(id=post_id)
    name_post = post.text[0:31]
    user = get_object_or_404(User, username=post.author)
    count_posts = len(user.posts.all())

    context = {
        'post': post,
        'name_post': name_post,
        'count_posts': count_posts,
    }
    return render(request, 'posts/post_detail.html', context)
