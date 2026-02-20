from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db.models import F, Q, Sum
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from .models import Post, PostView, Tag
from .forms import PostForm
from apps.categories.models import Category




class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_object(self, queryset=None):
        post = super().get_object()
        request = self.request
        user = request.user
        ip = request.META.get("REMOTE_ADDR")

        if user.is_authenticated:
            already_viewed = PostView.objects.filter(
                post=post,
                user=user
            ).exists()

            if not already_viewed:
                PostView.objects.create(post=post, user=user)
                Post.objects.filter(pk=post.pk).update(
                    views_count=F("views_count") + 1
                )

        else:
            already_viewed = PostView.objects.filter(
                post=post,
                ip_address=ip
            ).exists()

            if not already_viewed:
                PostView.objects.create(post=post, ip_address=ip)
                Post.objects.filter(pk=post.pk).update(
                    views_count=F("views_count") + 1
                )

        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Related news from the same category
        context['related_posts'] = Post.objects.filter(
            category=self.object.category
        ).exclude(pk=self.object.pk).order_by("-created_at")[:5]
        
        # Most viewed news in this category
        context['category_most_viewed'] = Post.objects.filter(
            category=self.object.category
        ).order_by("-views_count")[:5]
        
        # Most read across all categories for sidebar
        context['all_most_viewed'] = Post.objects.order_by("-views_count")[:10]
        
        # Latest news for sidebar
        context['latest_posts'] = Post.objects.order_by("-created_at")[:10]
        
        return context


class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "dashboard/post_form.html"
    success_url = reverse_lazy("dashboard")

    def test_func(self):
        # Admin can always post, others need can_post permission
        return self.request.user.role == "admin" or self.request.user.can_post()

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            # User is logged in but has no permission (subscription)
            return redirect("pricing")
        return super().handle_no_permission()

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 'pending'  # Yangi postlar tekshiruvda
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "dashboard/post_form.html"
    success_url = reverse_lazy("dashboard")

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("dashboard")

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

class PostSearchView(ListView):
    model = Post
    template_name = "posts/search_results.html"
    context_object_name = "posts"
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            ).order_by("-created_at")
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q")
        return context


post_detail_view = PostDetailView.as_view()
post_search_view = PostSearchView.as_view()
post_create_view = PostCreateView.as_view()
post_update_view = PostUpdateView.as_view()
post_delete_view = PostDeleteView.as_view()






