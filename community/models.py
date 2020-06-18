from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator # IntergerField의 범위를 설정하기 위함

from django.conf import settings
from movies.models import Movie

# dummy data
from faker import Faker
f = Faker('ko_KR')

class Review(models.Model):
    content = models.CharField(max_length=100)
    rate = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # user 와 1 : N
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # movie 와 1 : N
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    @classmethod
    def dummy(cls, n):
        for _ in range(n):
            cls.objects.create(
                content = f.text(),
                rate = f.random_int(min=1, max=10),
                user_id = f.random_int(min=2, max=12),
                movie_id = f.random_int(min=3, max=69),
            )


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # user 와 1 : N
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # movie 와 1 : N
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, blank=True)
    # 좋아요
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'like_reivews')

    @classmethod
    def dummy(cls, n):
        for _ in range(n):
            cls.objects.create(
                title = f.text(),
                content = f.text(),
                user_id = f.random_int(min=2, max=12),
                movie_id = f.random_int(min=3, max=69),
            )


class Comment(models.Model):
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # user 와 1 : N
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # article 과 1 : N
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    @classmethod
    def dummy(cls, n):
        for _ in range(n):
            cls.objects.create(
                content = f.text(),
                user_id = f.random_int(min=2, max=12),
                article_id = f.random_int(min=1, max=122),
            ) 

class Iwantthis(models.Model):
    comment = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 