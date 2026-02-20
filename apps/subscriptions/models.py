from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta




from django.db import models


class Tariff(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    duration_days = models.IntegerField(default=30)  # tarif muddati
    sms_limit = models.IntegerField(default=0)       # sms paketi

    can_post = models.BooleanField(default=False)
    can_sms = models.BooleanField(default=False)
    can_email = models.BooleanField(default=False)
    post_limit = models.IntegerField(default=0)  # max postlar soni

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions"
    )
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE)

    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    sms_used = models.IntegerField(default=0)

    def activate(self):
        self.start_date = timezone.now()
        self.end_date = self.start_date + timedelta(days=self.tariff.duration_days)
        self.is_active = True
        self.save()

    def is_valid(self):
        if not self.is_active:
            return False
        if self.end_date and self.end_date < timezone.now():
            return False
        return True

    def sms_left(self):
        return max(self.tariff.sms_limit - self.sms_used, 0)

    def __str__(self):
        return f"{self.user} - {self.tariff}"