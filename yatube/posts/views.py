from django.shortcuts import render, get_object_or_404, reverse
from django.forms import modelformset_factory
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .forms import PostForm
from .models import Post, Group, User


OUTPUT_COUNT = 10


def index(request):
    template = 'posts/index.html'

    post_list = Post.objects.all()

    paginator = Paginator(post_list, OUTPUT_COUNT)
    page_number = request.GET.get('page')
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
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)

    post_list = author.posts.all()

    paginator = Paginator(post_list, OUTPUT_COUNT)
    page_number = request.GET.get('page')
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
    name_post = post.text[:30]
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
    form = PostForm()
    template = 'posts/create_post.html'
    context = {'form': form,
               'title': 'Создание поста'}

    if request.method == 'POST':
        user = get_object_or_404(User, username=request.user.username)
        form = PostForm(request.POST)

        if form.is_valid():
            text = form.cleaned_data['text']
            group = form.cleaned_data['group']
            author = user
            Post.objects.create(author=author, text=text,
                                group=group)
            return HttpResponseRedirect(reverse('posts:profile', args=(author,)))

        context['form'] = form
        return render(request, template, context)

    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    post = Post.objects.get(id=post_id)
    author = get_object_or_404(User, username=post.author)
    user = get_object_or_404(User, username=request.user.username)

    if author.username == user.username:
        template = 'posts/create_post.html'
        form = PostForm(request.POST)
        context = {'form': form,
                   'title': 'Изменение поста',
                   'is_edit': True}

        if request.method == 'POST' and form.is_valid():
            post.text = form.cleaned_data['text']
            post.group = form.cleaned_data['group']
            post.save()
            return HttpResponseRedirect(reverse('posts:post_detail', args=(post_id,)))
        elif request.method != 'POST':
            form = PostForm(initial={'text': post.text,
                                     'group': post.group})
            context['form'] = form
            return render(request, template, context)

        return render(request, template, context)

    return HttpResponseRedirect(reverse('posts:post_detail', args=(post_id,)))
