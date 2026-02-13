from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('post/', include("apps.posts.urls")),
    # path('categories/', include("apps.categories.urls")),
    # path('tags/', include("apps.tags.urls")),
    # path('accounts/', include("apps.accounts.urls")),
    # path('payments/', include("apps.payments.urls")),
    # path('subscriptions/', include("apps.subscriptions.urls")),
    # path('sms/', include("apps.sms.urls")),
]
