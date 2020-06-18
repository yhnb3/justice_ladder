from django.urls import path
from . import views

app_name = "community"

urlpatterns = [

    # path('', views.index, name='index'), #### 테스트하려고 만든 페이지입니다.
    path('<int:movie_pk>/movie_detail', views.movie_detail, name="movie_detail"),   #### movie detail에서 한줄평과 article 5개 보여주는거 간단하게 만들어 놨습니다.

    # create
    path('<int:movie_pk>/article_create', views.article_create, name="article_create"),   #### 상세리뷰 생성
    path('<int:article_pk>/comment_create', views.comment_create, name="comment_create"),   #### 댓글 생성
    path('<int:movie_pk>/review_create', views.review_create, name="review_create"),    #### 한줄평 생성

   # read
    path('<int:movie_pk>/article_list', views.article_list, name="article_list"),   #### 해당 영화의 모든 상세리뷰 보기
    path('<int:article_pk>/article_detail', views.article_detail, name='article_detail'),    #### 상세리뷰의 detail 보기
    # path('<int:movie_pk>/review_list', views.review_list, name="review_list"),   #### 해당 영화의 모든 한줄평 보기
    path('', views.all_of_article, name="all_of_article"),    #### 모든 영화의 모든 상세리뷰 보기

    # update 일단 네이버 영화에는 comment 수정은 구현되어 있지 않아서 안 만들었습니다.
    path('<int:article_pk>/article_update', views.article_update, name="article_update"),   #### 상세리뷰 수정
    path('<int:review_pk>/review_update', views.review_update, name="review_update"),   #### 한줄평 수정
    path('<int:comment_pk>/comment_update', views.comment_update, name="comment_update"),   #### 코멘트 수정

    # delete
    path('<int:article_pk>/article_delete', views.article_delete, name="article_delete"),   #### 상세리뷰 삭제
    path('<int:comment_pk>/comment_delete', views.comment_delete, name="comment_delete"),   #### 댓글 삭제
    path('<int:review_pk>/review_delete', views.review_delete, name="review_delete"),   #### 한줄평 삭제

    # like
    path('<int:article_pk>/like',views.like, name="like"),    #### 좋아요

    ## user want
    path('userwant/', views.userwant, name="userwant"),
]
