from django.urls import path
from apps.posts.views import (
    post_detail_view, 
    post_search_view,
    post_create_view,
    post_update_view,
    post_delete_view
)

urlpatterns = [
    path('search/', post_search_view, name='post_search'),
    path('add/', post_create_view, name='post_create'),
    path('edit/<int:pk>/', post_update_view, name='post_update'),
    path('delete/<int:pk>/', post_delete_view, name='post_delete'),
    path('<slug:slug>/', post_detail_view, name='post_detail'),
]
