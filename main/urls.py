from django.urls import path

from . import views

app_name = "main"
urlpatterns = [
    path('', views.intro, name="intro"),
    path('search/', views.search, name="search"),
    path('about/', views.about, name="about"),
]