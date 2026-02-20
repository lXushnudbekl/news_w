from django.urls import path
from .views import PricingView, PurchaseTariffView

urlpatterns = [
    path('pricing/', PricingView.as_view(), name='pricing'),
    path('purchase/', PurchaseTariffView.as_view(), name='purchase_tariff'),
]
