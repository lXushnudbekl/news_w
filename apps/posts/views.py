from django.views.generic import DetailView, ListView
from django.db.models import F
from .models import Post, PostView




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


post_detail_view = PostDetailView.as_view()






