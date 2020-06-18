import os
import sys
import urllib.request
import requests
import json

from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse

from .models import Genre, Movie
from .forms import MovieForm
from community.models import Iwantthis
from decouple import config

SECRET_KEY = config('SECRET_KEY')
TMDB_KEY= config('TMDB_KEY')
NAVER_CLIENT_KEY= config('NAVER_CLIENT_KEY')
NAVER_CLIENT_SECRET= config('NAVER_CLIENT_SECRET')

# Create your views here.
def movie_edit(request, pk):
    if not request.user.is_staff:
        return redirect('main:intro')
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            movie = form.save()
            return redirect('movies:movie_index')
    else:
        form = MovieForm(instance=movie)
    context = {
        'form' : form,
    }
    return render(request, 'movies/movie_edit.html', context)


def getgenre(request):
    # 장르 가져오는 것으로 최초 서버에서 1회만 실행 하면된다.
    if not request.user.is_staff:
        return redirect('main:intro')
    url = "http://api.themoviedb.org/3/genre/movie/list?api_key=" + TMDB_KEY 
    res = requests.get(url)
    genre_json = json.loads(res.text)
    for genre in genre_json['genres']:
        Genre.objects.create(id=genre['id'], name=genre['name'])
    return render(request, "movies/movie_index.html")

def movie_index(request):
    movies = Movie.objects.all()
    context = {
        'movies' : movies,
    }
    return render(request, 'movies/movie_index.html', context)

def patchmovie(request):
    if not request.user.is_staff:
        return redirect('main:intro')
    title = request.GET.get('title')
    rate = request.GET.get('rate')
    poster_url = request.GET.get('poster_url')
    movie_id = request.GET.get('movie_id')
    director = request.GET.get('director')
    director = director[:-1]
    genres = request.GET.get('genres')
    pub_date = request.GET.get('pub_date')
    actor = request.GET.get('actor')
    actor = actor[:-1]
    genres = genres[1:-1]
    genres = genres.split(', ')
    rate = float(rate)
    movie = Movie.objects.create(title=title, user_rate=rate, pub_date=pub_date, movie_id=movie_id, director=director, actor=actor, poster_path=poster_url)    
    for i in genres:
        movie.genres.add(int(i))
    message = {
        'message' : 'ok'
    }
    return JsonResponse(message)


def movie_delete(request, pk):
    if not request.user.is_staff:
        return redirect('main:intro')
    movie = get_object_or_404(Movie, pk=pk)
    movie.delete()
    return redirect('movies:movie_index')

def movie_admin(request):
    if not request.user.is_staff:
        return redirect('main:intro')
    return render(request, 'movies/movie_admin.html')

def getmovie(request):
    if not request.user.is_staff:
        return redirect('main:intro')
    movie_title = request.GET.get('movie_title')
    if movie_title != '':
        client_id = NAVER_CLIENT_KEY
        client_secret = NAVER_CLIENT_SECRET
        encText = urllib.parse.quote(movie_title)
        url = "https://openapi.naver.com/v1/search/movie.json?query=" + encText 
        request_url = urllib.request.Request(url)
        request_url.add_header("X-Naver-Client-Id",client_id)
        request_url.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(request_url)
        rescode = response.getcode()
        if(rescode==200):
            API_KEY = TMDB_KEY
            response_body = response.read()
            result = json.loads(response_body.decode('utf-8'))
            movie_list = []
            movie_id = []
            for item in result['items']:
                if item['subtitle'] != "":
                    movie_subtitle = item['subtitle'].split(' ')
                    title_query = '+'.join(movie_subtitle)
                    tmdb_url = f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title_query}'
                    res = requests.get(tmdb_url)
                    movies_json = json.loads(res.text)
                    for tmdb_result in movies_json['results']:
                        if tmdb_result not in movie_list:
                            movie_list.append(tmdb_result)
                    # movie_list = movies_json.get('results')
            context = {
                'Tmdb_movies': movie_list,
                'naver_movies': result['items']
            }
            return render(request, 'movies/movie_admin.html', context)
        else:
            return redirect("movies:movie_index")
    else:
        return redirect("movies:movie_admin")


def userwant(request):
    userwant = Iwantthis.objects.all()
    context = {
        'userwant' : userwant,
    }
    return render(request, 'movies/userwant.html', context)


def userwant_delete(request, pk):
    if not request.user.is_staff:
        return redirect('main:intro')
    userwant = get_object_or_404(Iwantthis, pk=pk)
    userwant.delete()
    return redirect('movies:userwant')