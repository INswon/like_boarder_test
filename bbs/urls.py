# bbs/urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'bbs'

urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('post_create/', views.PostCreate.as_view(), name='post_create'),
    path('post_detail/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('post/delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('like_post/', views.LikeForPostView.as_view(), name='like_post'),
]
