from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils import timezone

from apps.subscriptions.models import Subscription
from apps.categories.models import Category
from apps.posts.models import Post


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/user_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        # User subscription
        user_subscription = Subscription.objects.filter(
            user=user,
            is_active=True
        ).select_related("tariff").first()

        # Categories (SMS tanlash uchun)
        categories = Category.objects.filter(is_active=True)

        # Bugungi eng ko‘p ko‘rilgan post
        today = timezone.now().date()
        daily_top_post = (
            Post.objects.filter(created_at__date=today)
            .order_by("-views_count")
            .first()
        )

        # SMS yuborilganmi (keyin sms log bilan bog‘lanadi)
        already_sent = False

        context.update({
            "user_subscription": user_subscription,
            "categories": categories,
            "daily_top_post": daily_top_post,
            "already_sent": already_sent,
        })

        return context
