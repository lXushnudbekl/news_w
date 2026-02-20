from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Tariff, Subscription

class PricingView(TemplateView):
    template_name = "subscriptions/pricing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tariffs"] = Tariff.objects.exclude(code="free").order_by("price")
        return context

class PurchaseTariffView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        tariff_id = request.POST.get("tariff_id")
        tariff = Tariff.objects.get(id=tariff_id)
        
        # Deactivate old active subscriptions for this user
        Subscription.objects.filter(user=request.user, is_active=True).update(is_active=False)
        
        # Create new subscription
        subscription = Subscription.objects.create(
            user=request.user,
            tariff=tariff,
            is_active=True,
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=tariff.duration_days)
        )
        
        return redirect("dashboard")
