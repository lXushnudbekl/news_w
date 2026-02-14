from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.core.views import dashboard

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('post/', include("apps.posts.urls")),
]
