from django.contrib.auth import get_user_model
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.text import slugify
from apps.categories.models import Category
from apps.tags.models import Tag

from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string


class Post(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="posts/%Y/%m/%d", blank=True)
    description = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    views_count = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{get_random_string(4)}"
            self.slug = slug
        super().save(*args, **kwargs)



User = get_user_model()

class PostView(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="views")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user', 'ip_address')

    def __str__(self):
        return f"{self.post.title}"