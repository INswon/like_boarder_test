from django.db import models
from django.utils import timezone
from register.models import User
from django.views import generic
from django.shortcuts import redirect
from django.urls import reverse_lazy

class Post(models.Model):
    """投稿"""
    title = models.CharField('タイトル', max_length=256)
    text = models.TextField('本文')
    created_at = models.DateTimeField('作成日', default=timezone.now)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作成者')
    image = models.ImageField(upload_to='photos/')
    like_count = models.PositiveIntegerField('いいね数', default=0)  # 修正済み

    def __str__(self):
        return self.title
    
    def update_like_count(self):
        """いいね数を更新する"""
        self.like_count = self.likeforpost_set.count()


class Comment(models.Model):
    """コメント"""
    writer = models.CharField('名前', default='名無し', max_length=32)
    text = models.TextField('本文')
    target = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='対象記事')
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return self.text[:20]


class LikeForPost(models.Model):
    """投稿に対するいいね"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 修正済み

    class Meta:
        unique_together = ('post', 'user')  # 一人のユーザーが一つの投稿に対して複数回「いいね」できないようにする
        

class LikeForComment(models.Model):
    """コメントに対するいいね"""
    target = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)