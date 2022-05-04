from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from datetime import date

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
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()[:OUTPUT_COUNT]
    paginator = Paginator(post_list, OUTPUT_COUNT)

    if request.GET.get('page'):
        page_number = request.GET.get('page')
    else:
        page_number = 1

    page_obj = paginator.get_page(page_number)
    count_posts = len(author.posts.all())
    context = {
        'author': author,
        'page_obj': page_obj,
        'count_posts': count_posts,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'

    post = Post.objects.get(id=post_id)
    name_post = post.text[0:31]
    user = get_object_or_404(User, username=post.author)
    count_posts = len(user.posts.all())

    context = {
        'post': post,
        'name_post': name_post,
        'count_posts': count_posts,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    if request.method == 'POST':
        user = get_object_or_404(User, username=request.user.username)
        form = PostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            pub_date = date.today()
            group = form.cleaned_data['group']
            author = user
            Post.objects.create(author=author, text=text, group=group, pub_date=pub_date)
            return redirect(f'/profile/{author}/')
        else:
            template = 'posts/create_post.html'
            context = {'form': form,
                       'title': 'Создание поста'}
            return render(request, template, context)

    template = 'posts/create_post.html'
    form = PostForm()
    context = {'form': form,
               'title': 'Создание поста'}
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    post = Post.objects.get(id=post_id)
    author = get_object_or_404(User, username=post.author)
    user = get_object_or_404(User, username=request.user.username)

    if author.username == user.username:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post.text = form.cleaned_data['text']
                post.pub_date = date.today()
                post.group = form.cleaned_data['group']
                post.save()

                return redirect(f'/posts/{post_id}/')
            else:
                template = 'posts/create_post.html'
                context = {'form': form,
                           'title': 'Изменение поста',
                           'is_edit': True}
                return render(request, template, context)
        else:
            template = 'posts/create_post.html'
            form = PostForm(initial={'text': post.text,
                                     'group': post.group})
            context = {'form': form,
                       'title': 'Изменение поста',
                       'is_edit': True}
            return render(request, template, context)

    return redirect(f'/posts/{post_id}/')
