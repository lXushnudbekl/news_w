from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, CreateView
from django.db.models import Sum
from django.utils import timezone

from apps.subscriptions.models import Subscription, Tariff
from apps.categories.models import Category
from apps.posts.models import Post
from .forms import UserProfileForm, UserRegisterForm, UserLoginForm


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/user_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        # User subscriptions history or active
        active_subscription = Subscription.objects.filter(
            user=user,
            is_active=True
        ).select_related("tariff").first()

        # User's own posts
        user_posts = Post.objects.filter(author=user).order_by("-created_at")
        
        # Stats
        total_posts = user_posts.count()
        total_views = user_posts.aggregate(Sum('views_count'))['views_count__sum'] or 0
        most_popular = user_posts.order_by("-views_count").first()

        # SMS section (mock for now as per models.py being empty)
        sms_subscription = active_subscription if active_subscription and active_subscription.tariff.can_sms else None

        context.update({
            "active_subscription": active_subscription,
            "posts": user_posts,
            "total_posts": total_posts,
            "total_views": total_views,
            "most_popular": most_popular,
            "sms_subscription": sms_subscription,
            "categories": Category.objects.filter(is_active=True),
        })

        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserProfileForm
    template_name = "dashboard/profile_settings.html"
    success_url = reverse_lazy("dashboard")

    def get_object(self, queryset=None):
        return self.request.user

class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "dashboard/profile_settings.html"
    success_url = reverse_lazy("dashboard")

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
                end_date=timezone.now() + timezone.timedelta(days=365) # 1 year free
            )
        
        login(self.request, user)
        return redirect(self.success_url)

class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = UserLoginForm

    def get_success_url(self):
        if self.request.user.is_superuser:
            return "/admin/"
        return reverse_lazy("dashboard")

def logout_view(request):
    logout(request)
    return redirect("login")
