from django.urls import path
from apps.posts.views import post_detail_view

urlpatterns = [
    path('post/<slug:slug>/', post_detail_view, name='post_detail'),
]