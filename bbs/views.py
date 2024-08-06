from django.views import generic
from .models import Post, LikeForPost
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View

class PostList(generic.ListView):
    template_name = 'bbs/post_list.html'
    model = Post

class PostDetail(generic.DetailView):
    template_name ='bbs/post_detail.html'
    model = Post

class PostCreate(generic.CreateView):
    template_name="bbs/post_create.html"
    fields = ['writer','title','text','image'] 
    model = Post
    success_url = reverse_lazy('bbs:post_list')

    def form_valid(self, form):
        form.instance.writer = self.request.user
        return super().form_valid(form)

class PostDeleteView(generic.DeleteView):
    model = Post
    template_name = 'bbs/post_delete.html'
    success_url = reverse_lazy('bbs:post_list')

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        self.reset_sequence()
        return response
    
    def reset_sequence(self):
        # シーケンスリセットの処理
        with connection.cursor() as cursor:
            cursor.execute("SELECT setval(pg_get_serial_sequence('yourapp_post', 'id'), coalesce(max(id), 1) + 1, false) FROM yourapp_post;")

class LikeForPostView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        post_pk = request.POST.get('post_pk')
        post = get_object_or_404(Post, pk=post_pk)
        user = request.user

        like = LikeForPost.objects.filter(post=post, user=user)

        if like.exists():
            like.delete()
            action = 'deleted'
        else:
            LikeForPost.objects.create(post=post, user=user)
            action = 'created'

        post.like_count = LikeForPost.objects.filter(post=post).count()
        post.save()

        return JsonResponse({'like_count': post.like_count, 'action': action})
