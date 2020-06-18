import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse

from .forms import ArticleForm, CommentForm, ReviewForm, IwantthisForm
from .models import Article, Comment, Review, Iwantthis
from movies.models import Movie


# def index(request):
#     articles = Article.objects.all()
#     reviews = Review.objects.all()
#     comments = Comment.objects.all()
#     context = {
#         'articles' : articles,
#         'reviews' : reviews,
#         'comments' : comments,
#     }
#     return render(request, 'community/index.html', context)


#### movie detail에서 한줄평과 article 5개 보여주는거 간단하게 만들어 놨습니다.
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk = movie_pk)
    articles = Article.objects.filter(movie = movie)
    now_date = datetime.datetime.now().strftime('%Y-%m-%d')
    reviews = Review.objects.filter(movie = movie).order_by('-id')
    paginator = Paginator(reviews, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    genres = movie.genres.all()
    movie_gen = []
    for i in genres:
        movie_gen.append(i.name)
    movie_genres = ' | '.join(movie_gen)

    form = ReviewForm()
    ### 5개 이상이면 5개만 가져오기
    if articles.count() >= 5:
        articles = articles[:5]
    context = {
        'movie' : movie,
        'movie_genres': movie_genres,
        'articles' : articles,
        'reviews' : page_obj,
        'form' : form,
        'now_date': now_date,
        'key': 'AIzaSyB4ulLEBtGaIjqQpJNFkY8n2-bWgqb_Rhc'
    }
    return render(request, 'community/movie_detail.html', context)


###### create ######


@login_required
def article_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk = movie_pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.movie = movie
            article.save()
            return redirect('community:article_detail', article.pk)
    else:
        form = ArticleForm()
    context = {
        'form' : form,
    }
    return render(request, 'community/form.html', context)


@login_required
def comment_create(request, article_pk):
    article = get_object_or_404(Article, pk = article_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.article = article
            comment.save()
            return redirect('community:article_detail', article.pk)
    else:
        form = CommentForm()
    context = {
        'form' : form,
    }
    return render(request, 'community/article_detail', context)


@login_required
def review_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk = movie_pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            return redirect('community:movie_detail', movie.pk)
    else:
        form = ReviewForm()
    context = {
        'form' : form,
    }
    return render(request, 'community/form.html', context)


###### create ######
###### read ######


def article_list(request, movie_pk):
    article_title = request.GET.get('article_title')
    movie = get_object_or_404(Movie, pk = movie_pk)
    articles = Article.objects.filter(movie = movie).order_by('-created_at')
    if article_title != None:
        articles = Article.objects.filter(title__icontains=article_title).order_by('-created_at')
    paginator = Paginator(articles, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'articles' : articles,
        'page_obj' : page_obj,
        'movie' : movie,
    }
    return render(request, 'community/article_list.html', context)


def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk = article_pk)
    comment_form = CommentForm()
    context = {
        'article' : article,
        'comment_form' : comment_form,
    }
    return render(request, 'community/article_detail.html', context)


def review_list(request, movie_pk):
    movie = get_object_or_404(Movie, pk = movie_pk)
    reviews = Review.objects.filter(movie = movie).order_by('id')

    paginator = Paginator(reviews, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = ReviewForm()

    context = {
        'reviews' : reviews,
        'page_obj' : page_obj,
        'form' : form,
        'movie' : movie,
    }
    return render(request, 'community/review_list.html', context)


def all_of_article(request):
    movie_title = request.GET.get('movie_title')
    article_title = request.GET.get('article_title')
    now_date = datetime.datetime.now().strftime('%Y-%m-%d')
    articles = []
    if movie_title != None:
        movies = Movie.objects.filter(title__icontains=movie_title)
        if len(movies) != 0:
            articles = movies[0].article_set.order_by('-created_at')
        for i in range(1, len(movies)):
            articles = articles | movies[i].article_set.order_by('-created_at')
    elif article_title != None:
        articles = Article.objects.filter(title__icontains=article_title).order_by('-created_at')
    else:
        articles = Article.objects.order_by('-created_at')    ####### 수정시간기준 최신순으로 보여줍니다
    paginator = Paginator(articles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'articles' : articles,
        'page_obj' : page_obj,
        'now_date' : now_date,
    }
    return render(request, 'community/all_of_article.html', context)


###### read ######
###### update ######


@login_required
def article_update(request, article_pk):
    article = get_object_or_404(Article, pk = article_pk)
    if request.user == article.user:
        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                article = form.save()
                return redirect('community:article_detail', article.pk)
        else:
            form = ArticleForm(instance=article)
        context = {
            'form' : form,
        }
        return render(request, 'community/form.html', context)
    else:
        return redirect('main:intro')


@login_required
def review_update(request, review_pk):
    review = get_object_or_404(Review, pk = review_pk)
    if request.user == review.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                review = form.save()
                return redirect('community:movie_detail', review.movie.pk)
        else:
            form = ReviewForm(instance=review)
        context = {
            'form' : form,
        }
        return render(request, 'community/form.html', context)
    else:
        return redirect('main:intro')


@login_required
def comment_update(request, comment_pk):
    comment = get_object_or_404(Comment, pk = comment_pk)
    if request.user == comment.user:
        if request.method == 'POST':
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                comment = form.save()
                return redirect('community:article_detail', comment.article.pk)
        else:
            form = CommnetForm(instance=comment)
        context = {
            'form' : form,
        }
        return render(request, 'community/form.html', context)
    else:
        return redirect('main:intro')


###### update ######
###### delete ######


@login_required
def article_delete(request, article_pk):
    article = get_object_or_404(Article, pk = article_pk)
    movie = article.movie
    if request.user == article.user:
        article.delete()
        return redirect('community:article_list', movie.pk)
    else:
        return redirect('main:intro')


@login_required
def review_delete(request, review_pk):
    review = get_object_or_404(Review, pk = review_pk)
    movie = review.movie
    if request.user == review.user:
        review.delete()
        return redirect('community:movie_detail', movie.pk)
    else:
        return redirect('main:intro')


@login_required
def comment_delete(request, comment_pk):
    comment = get_object_or_404(Comment, pk = comment_pk)
    article = comment.article
    if request.user == comment.user:
        comment.delete()
        return redirect('community:article_detail', article.pk)
    else:
        return redirect('main:intro')


###### delete ######
###### like ######


@login_required
def like(request, article_pk):
    # user = 로그인되어있는사람
    user = request.user
    article = get_object_or_404(Article, pk = article_pk)

    if article.like_users.filter(pk=user.pk).exists():
        article.like_users.remove(user)
        liked = False
    else:
        article.like_users.add(user)
        liked = True

    context = {
        'liked' : liked,
        'count' : article.like_users.count(),
    }
    return JsonResponse(context)


def article_clean(request):
    articles = Article.objects.all()
    for article in articles:
        if len(article.title) > 70:
            article.title = article.title[:70]
            article.save()
    return render(request, 'community/all_of_article.html')

## user want
@login_required
def userwant(request):
    if request.method == 'POST':
        form = IwantthisForm(request.POST)
        if form.is_valid():
            iwantthis = form.save(commit=False)
            iwantthis.user = request.user
            iwantthis.save()
            return redirect('main:intro')
    else:
        form = IwantthisForm()
    context = {
        'form' : form,
    }
    return render(request, 'community/form.html', context)