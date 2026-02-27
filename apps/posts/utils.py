from apps.sms.models import SMSCategorySubscription
from apps.sms.utils import send_user_sms


def notify_sms_users(post):
    subs = SMSCategorySubscription.objects.filter(category=post.category)

    for sub in subs:
        user = sub.user
        text = f"Yangi {post.category.name}: {post.title}"
        send_user_sms(user, text)