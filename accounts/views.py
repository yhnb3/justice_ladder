import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage

from .forms import CustomUserCreationForm, CustomUserChangeForm

from community.models import Review, Article


def signup(request):
    if request.user.is_authenticated:
        return redirect('main:intro')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('main:intro')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('main:intro')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'main:intro')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


def logout(request):
    if not request.user.is_authenticated:
        return redirect('main:intro')
    auth_logout(request)
    return redirect('main:intro')



def edit(request):
    if not request.user.is_authenticated:
        return redirect('main:intro')
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            if user.photo == '':
                user.photo = 'images/custom_no_image.jpg'
                user.save()
            return redirect('accounts:detail', request.user.nickname)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/edit.html', context)


def detail(request, user_name):
    User = get_user_model()
    user = get_object_or_404(User, nickname=user_name)
    reviews = user.review_set.all()
    followings = user.followings.values_list('id', flat=True)
    articles1 = Article.objects.filter(user_id__in=followings).order_by('-created_at')
    page_num = request.GET.get('page_num')
    page_num = 1
    paginator = Paginator(articles1, 7)
    articles = paginator.page(page_num)
    context = {
        'user': user,
        'reviews': reviews,
        'articles': articles,
        'has_next': articles.has_next(),
    }
    return render(request, 'accounts/detail.html', context)


def load_more(request, user_name):
    # get datas
    User = get_user_model()
    user = get_object_or_404(User, nickname=user_name)
    followings = user.followings.values_list('id', flat=True)
    articles1 = Article.objects.filter(user_id__in=followings).order_by('-created_at')

    # make page obj
    page_num = request.GET.get('page_num')
    paginator = Paginator(articles1, 7)
    articles2 = paginator.page(page_num)

    # make obj to need data
    articles = []
    for article in articles2:
        articles.append({
            'movie_pk': article.movie.pk,
            'movie_poster': article.movie.poster_path,
            'article_pk': article.pk,
            'article_title': article.title,
            'user_nickname': article.user.nickname,
            'user_image': article.user.image_thumbnail.url,
            'liked': True if user in article.like_users.all() else False,
            'like_num': len(article.like_users.all()),
            'has_next': articles2.has_next(),
        })
    articles = json.dumps(articles)
    context = {
        'articles': articles
    }
    return JsonResponse(context)


@login_required
def follow(request, user_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=user_pk)
    # 스스로를 팔로우 할 수 없음.
    if user != request.user:
        if user.followers.filter(pk=request.user.pk).exists():
            user.followers.remove(request.user)
        else:
            user.followers.add(request.user)
    return redirect('accounts:detail', user.nickname)