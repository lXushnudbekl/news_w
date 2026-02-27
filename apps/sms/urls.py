from django.urls import path
from .views import sms_category_subscribe

urlpatterns = [
    path("subscribe/", sms_category_subscribe, name="sms_category_subscribe"),
]