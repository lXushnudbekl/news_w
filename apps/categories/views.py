from django.views.generic import ListView

from apps.posts.models import Post


class CategoryPostView(ListView):
    model = Post
    template_name = "posts/category_posts.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(
            status='published',
            category__slug=self.kwargs['slug']
        ).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from apps.categories.models import Category
        context['category'] = Category.objects.filter(slug=self.kwargs['slug']).first()
        return context


category_post_view = CategoryPostView.as_view()
