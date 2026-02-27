from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, CreateView
from django.db.models import Sum
from django.utils import timezone
from django.views import View
from django.http import JsonResponse
from django.db.models import Q
from apps.subscriptions.models import Subscription, Tariff
from apps.categories.models import Category
from apps.posts.models import Post
from .forms import UserProfileForm, UserRegisterForm, UserLoginForm


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/user_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        # ✅ Active subscription
        active_subscription = (
            Subscription.objects
            .filter(user=user, is_active=True)
            .select_related("tariff")
            .first()
        )

        # ✅ USER POSTS QUERYSET (full for stats)
        user_posts_qs = Post.objects.filter(author=user).order_by("-created_at")

        # ✅ PAGINATION
        paginator = Paginator(user_posts_qs, 5)  # har sahifa 10 post
        page_number = self.request.GET.get("page")
        posts_page = paginator.get_page(page_number)

        # ✅ STATS (full querysetdan)
        total_posts = user_posts_qs.count()
        total_views = user_posts_qs.aggregate(
            total=Sum("views_count")
        )["total"] or 0

        most_popular = user_posts_qs.order_by("-views_count").first()

        # ✅ SMS
        sms_subscription = (
            active_subscription
            if active_subscription and active_subscription.tariff.can_sms
            else None
        )

        # ✅ CONTEXT
        context.update({
            "active_subscription": active_subscription,
            "posts": posts_page,       # template loop uchun
            "page_obj": posts_page,    # pagination.html uchun ⭐
            "total_posts": total_posts,
            "total_views": total_views,
            "most_popular": most_popular,
            "sms_subscription": sms_subscription,
            "categories": Category.objects.filter(is_active=True),
        })

        return context

dashboard_view = DashboardView.as_view()

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserProfileForm
    template_name = "dashboard/profile_settings.html"
    success_url = reverse_lazy("dashboard")

    def get_object(self, queryset=None):
        return self.request.user
profile_update_view = ProfileUpdateView.as_view()

class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "dashboard/password_change.html"
    success_url = reverse_lazy("dashboard")
user_password_change_view = UserPasswordChangeView.as_view()

class UserRegisterView(CreateView):
    model = get_user_model()
    form_class = UserRegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        # Assign FREE subscription
        free_tariff = Tariff.objects.filter(code__iexact="free").first()
        if free_tariff:
            Subscription.objects.create(
                user=user,
                tariff=free_tariff,
                is_active=True,
                end_date=timezone.now() + timezone.timedelta(days=365)  # 1 year free
            )

        login(self.request, user)
        return redirect(self.success_url)

register_view = UserRegisterView.as_view()
class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = UserLoginForm

    def get_success_url(self):
        user = self.request.user



        return reverse_lazy("dashboard")
user_login_view = UserLoginView.as_view()

class LiveSearchView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get("q", "").strip()

        results = []

        if q:
            posts = Post.objects.filter(
                Q(title__icontains=q),
                status="published"
            )[:5]

            results = [
                {
                    "title": p.title,
                    "slug": p.slug,
                    "image": p.image.url if p.image else ""
                }
                for p in posts
            ]

        return JsonResponse({"results": results})

live_search_view = LiveSearchView.as_view()
def logout_view(request):
    logout(request)
    return redirect("login")
