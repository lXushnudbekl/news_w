from django.shortcuts import render
from django.views.generic import ListView, DetailView

from apps.posts.models import Post


class HomeView(ListView):
    model = Post
    template_name = 'posts/list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

home_view = HomeView.as_view()

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        post.views_count += 1
        post.save(update_fields=['views_count'])
        return post
post_detail_view = PostDetailView.as_view()