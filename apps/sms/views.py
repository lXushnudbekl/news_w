from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.categories.models import Category
from apps.subscriptions.models import Subscription
from .models import SMSCategorySubscription


class SMSCategorySubscribeView(LoginRequiredMixin, View):
    def post(self, request):
        category_id = request.POST.get("category_id")

        if not category_id:
            return redirect("dashboard")

        category = Category.objects.get(id=category_id)

        sub = Subscription.objects.filter(
            user=request.user,
            tariff__can_sms=True,
            is_active=True
        ).first()

        if not sub:
            return redirect("dashboard")

        SMSCategorySubscription.objects.update_or_create(
            user=request.user,
            defaults={
                "category": category,
                "subscription": sub
            }
        )

        return redirect("dashboard")
sms_category_subscribe = SMSCategorySubscribeView.as_view()