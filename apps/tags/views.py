from django.views.generic import ListView

from .models import Tag
from ..posts.models import Post


class TagPostListView(ListView):
    model = Post
    template_name = "posts/tag_posts.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        return (
            Post.objects
            .select_related("category")
            .prefetch_related("tags")
            .filter(tags__slug=slug)
            .order_by("-created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get("slug")
        context["tag"] = Tag.objects.get(slug=slug)
        return context
