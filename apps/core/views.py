from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Q, F, IntegerField, ExpressionWrapper
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
            .filter(status="published")
            .order_by("-created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        now = timezone.now()
        last_month = now - timedelta(days=30)
        week_ago = now - timedelta(days=7)

        # ⭐ Tavsiya (net likes)
        recommended = Post.objects.filter(
            status="published",
            created_at__gte=last_month
        ).annotate(
            likes_agg=Count("reactions", filter=Q(reactions__value=1)),
            dislikes_agg=Count("reactions", filter=Q(reactions__value=-1)),
        ).annotate(
            net_likes=ExpressionWrapper(
                F("likes_agg") - F("dislikes_agg"),
                output_field=IntegerField()
            )
        ).order_by("-net_likes", "-views_count")[:5]

        # ⭐ Haftalik eng ko‘p like
        weekly_top = Post.objects.filter(
            status="published",
            created_at__gte=week_ago
        ).annotate(
            week_likes=Count(
                "reactions",
                filter=Q(
                    reactions__value=1,
                    reactions__created_at__gte=week_ago
                )
            )
        ).order_by("-week_likes", "-views_count")[:5]
        yesterday_start = (now - timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        yesterday_end = yesterday_start + timedelta(days=1)

        yesterday_posts = Post.objects.filter(
            status="published",
            created_at__gte=yesterday_start,
            created_at__lt=yesterday_end
        ).order_by("-created_at")

        context["yesterday_posts"] = yesterday_posts
        # ⭐ Trendda — haftalik eng ko‘p ko‘rilgan
        weekly_most_viewed = Post.objects.filter(
            status="published",
            created_at__gte=week_ago
        ).order_by("-views_count")[:10]

        context["recommended_posts"] = recommended
        context["weekly_top_posts"] = weekly_top
        context["sorted_posts"] = weekly_most_viewed

        return context


dashboard = Dashboard.as_view()
