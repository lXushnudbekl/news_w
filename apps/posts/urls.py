from django.urls import path
from apps.posts.views import post_detail_view, post_list_view

urlpatterns = [
    path('', post_list_view, name='post_list'),
    path('<slug:slug>/', post_detail_view, name='post_detail'),

]
