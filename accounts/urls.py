from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('edit/', views.edit, name='edit'),
    path('<int:user_pk>/follow/', views.follow, name='follow'),
    path('detail/<str:user_name>/', views.detail, name='detail'),
    path('<str:user_name>/load-more/', views.load_more, name='load_more'),
]