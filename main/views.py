import datetime

from django.shortcuts import render, get_object_or_404

from movies.models import Movie, Genre

def intro(request):
    # 평점순
    recommend_movie = []
    if request.user.is_authenticated:
        movies = []
        titles = []
        followings = request.user.followings.all()
        for i in followings:
            for j in i.article_set.all():
                if j.movie.title not in titles:
                    movies.append([j.movie.user_rate, j.movie.title, j.movie.movie_id])
                    titles.append(j.movie.title)
        movies.sort(reverse=True)
        for i in movies:
            movie = get_object_or_404(Movie, movie_id = i[2])
            recommend_movie.append(movie)
        all_movies = Movie.objects.order_by('-user_rate')
        if len(recommend_movie) < 6:
            for i in all_movies:
                if i.title not in titles:
                    recommend_movie.append(i)
                if len(recommend_movie) == 6:
                    break
        if len(recommend_movie) > 6:
            recommend_movie = recommend_movie[:6]
    # 시간대별 추천
    now_time = int(datetime.datetime.now().strftime('%H'))
    recommend_title = '아무거나 보세요 그냥'
    genre = Genre.objects.get(pk=16)
    if 0 <= now_time < 5:
        recommend_title = '뒤에 계신 그분은 누구시죠?'
        genre = Genre.objects.get(pk=27)
    elif 5 <= now_time < 10:
        recommend_title = '힘들 때 웃는 자가 일류다...ㅋㅋ'
        genre = Genre.objects.get(pk=35)
    elif 10 <= now_time < 14:
        recommend_title = '혼밥엔 역시 스릴러'
        genre = Genre.objects.get(pk=53)
    elif 14 <= now_time < 18:
        recommend_title = '나른한 오후에는 액션영화'
        genre = Genre.objects.get(pk=28)
    elif 18 <= now_time < 21:
        recommend_title = '평화로운 저녁, 달달한 염장질 그리고 소주'
        genre = Genre.objects.get(pk=10749)
    elif 21 <= now_time < 22:
        recommend_title = '헐ㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠ'
        genre = Genre.objects.get(pk=18)
    elif 22 <= now_time <= 24:
        recommend_title = '잘자요'
        genre = Genre.objects.get(pk=99)
    time_movies = genre.movies.order_by('-user_rate')
    if len(time_movies) > 6:
        time_movies = time_movies[:6]

    # 최신 영화
    new_movie = Movie.objects.all().order_by('-created_at')
    if new_movie.count() >= 6:
        new_movie = new_movie[:6]

    context = {
        'recommend_title': recommend_title,
        'movies': time_movies,
        'recommend_movie': recommend_movie,
        'new_movie' : new_movie,
    }
    return render(request, 'main/intro.html', context)


def search(request):
    movie_title = request.GET.get('movie_title')
    movies = Movie.objects.filter(title__icontains=movie_title)
    context = {
        'movie_title': movie_title,
        'movies': movies,
    }
    return render(request, 'main/search_result.html', context)


def about(request):
    return render(request, 'main/about.html')