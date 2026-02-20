from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from apps.subscriptions.models import Subscription

class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("user", "User"),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def active_subscriptions(self):
        return self.subscriptions.filter(
            is_active=True,
            end_date__gt=timezone.now()
        )

    def has_permission(self, perm):
        if self.role == "admin":
            return True

        return self.active_subscriptions().filter(
            tariff__can_post=True if perm == "post" else False,
            tariff__can_sms=True if perm == "sms" else False
        ).exists()

    def can_post(self):
        return self.has_permission("post")

    def can_sms(self):
        return self.has_permission("sms")
