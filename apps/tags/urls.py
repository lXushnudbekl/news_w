from django.urls import path
from .views import TagPostListView

urlpatterns = [
    path('<slug:slug>/', TagPostListView.as_view(), name='tag_posts'),
]
