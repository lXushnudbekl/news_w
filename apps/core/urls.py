from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.core.views import dashboard

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('category/', include("apps.categories.urls")),

    path('post/', include("apps.posts.urls")),
    path('profile/', include("apps.accounts.urls")),
    # path('categories/', include("apps.categories.urls")),
    path('tag/', include("apps.tags.urls")),
    # path('accounts/', include("apps.accounts.urls")),
    # path('payments/', include("apps.payments.urls")),
    path('subscriptions/', include("apps.subscriptions.urls")),
    # path('sms/', include("apps.sms.urls")),
]
