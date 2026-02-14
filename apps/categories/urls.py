from django.urls import path
from apps.categories.views import category_post_view

urlpatterns = [
    path('<slug:slug>/', category_post_view, name='category_posts'),

]
