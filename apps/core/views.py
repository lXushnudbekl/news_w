from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import F, ExpressionWrapper, IntegerField
from django.utils import timezone
from datetime import timedelta

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
            .filter(status='published')
            .order_by("-created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        last_month = timezone.now() - timedelta(days=30)
        
        # Recommendation logic: likes - dislikes, last 30 days
        recommended = Post.objects.filter(
            status='published',
            created_at__gte=last_month
        ).annotate(
            net_likes=ExpressionWrapper(F('likes') - F('dislikes'), output_field=IntegerField())
        ).order_by("-net_likes", "-views_count")[:5]

        context["recommended_posts"] = recommended
        return context

dashboard = Dashboard.as_view()