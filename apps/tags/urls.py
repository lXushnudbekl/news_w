from django.urls import path
from .views import  tag_post_view

urlpatterns = [
    path('<slug:slug>/', tag_post_view, name='tag_posts'),
]
