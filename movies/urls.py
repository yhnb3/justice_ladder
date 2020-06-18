from django.urls import path
from . import views

app_name ="movies"

urlpatterns = [
    path('', views.movie_index, name="movie_index"),
    path('administer/', views.movie_admin, name="movie_admin"),
    path('getmovie/', views.getmovie, name="getmovie"),
    path('getgenre/', views.getgenre, name="getgenre"),
    path('patchmovie/', views.patchmovie, name="patchmovie"),
    path('delete/<int:pk>/', views.movie_delete, name="movie_delete"),
    path('edit/<int:pk>/', views.movie_edit, name="movie_edit"),
    path('userwant/', views.userwant, name="userwant"),
    path('userwant_delete/<int:pk>/', views.userwant_delete, name="userwant_delete"),
]