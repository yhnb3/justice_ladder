from django.db import models

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    poster_path = models.CharField(max_length=200)
    director = models.CharField(max_length=200)
    actor = models.TextField()
    movie_id = models.IntegerField(unique=True)
    user_rate = models.FloatField()
    pub_date = models.IntegerField()
    genres = models.ManyToManyField(
        Genre,
        related_name = "movies"
    )
    created_at = models.DateTimeField(auto_now_add=True)


    
