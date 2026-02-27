from django.contrib.auth import get_user_model
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.text import slugify
from apps.categories.models import Category
from apps.tags.models import Tag

from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string

from apps.categories.models import Category
from apps.tags.models import Tag
from apps.sms.models import SMSCategorySubscription
from apps.sms.utils import send_user_sms

User = get_user_model()


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('published', 'Published')
    )

    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="posts/%Y/%m/%d", blank=True)
    description = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    views_count = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.title

    # 👇 SHU YERGA QO‘SHILADI
    @property
    def likes_count(self):
        return self.reactions.filter(value=PostReaction.LIKE).count()

    @property
    def dislikes_count(self):
        return self.reactions.filter(value=PostReaction.DISLIKE).count()

    def notify_sms(self):
        subs = SMSCategorySubscription.objects.filter(category=self.category)
        for sub in subs:
            user = sub.user
            text = f"Yangi {self.category.name}: {self.title}"
            send_user_sms(user, text)

class PostReaction(models.Model):
    LIKE = 1
    DISLIKE = -1

    VALUE_CHOICES = (
        (LIKE, "Like"),
        (DISLIKE, "Dislike"),
    )

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reactions")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=VALUE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return f"{self.user} → {self.post} ({self.value})"


class PostView(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="views")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user', 'ip_address')

    def __str__(self):
        return f"{self.post.title}"
