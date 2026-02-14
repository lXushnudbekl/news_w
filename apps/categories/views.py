# from django.views.generic import ListView
# from django.shortcuts import get_object_or_404
# from apps.posts.models import Post
# from apps.categories.models import Category
#
#
# class CategoryPostListView(ListView):
#     model = Post
#     template_name = "base.html"
#     context_object_name = "posts"
#     paginate_by = 6
#
#     def get_queryset(self):
#         self.category = get_object_or_404(
#             Category,
#             slug=self.kwargs["slug"]
#         )
#
#         return (
#             Post.objects
#             .filter(category=self.category)
#             .select_related("category")
#             .order_by("-created_at")
#         )
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["category"] = self.category
#         return context
#
from django.views.generic import ListView

from apps.posts.models import Post


class CategoryPostView(ListView):
    model = Post
    template_name = "posts/category_posts.html"
    context_object_name = "posts"
    paginate_by = 20

    def get_queryset(self):
        return Post.objects.filter(
            category__slug=self.kwargs['slug']
        ).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from apps.categories.models import Category
        context['category'] = Category.objects.filter(slug=self.kwargs['slug']).first()
        return context


category_post_view = CategoryPostView.as_view()
