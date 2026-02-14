from django.shortcuts import render
from django.views.generic import ListView

from apps.posts.models import Post


class Dashboard(ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"
    paginate_by = 40

    def get_queryset(self):
        return (
            Post.objects
            .select_related("category")
            .order_by("-created_at")
        )

dashboard = Dashboard.as_view()