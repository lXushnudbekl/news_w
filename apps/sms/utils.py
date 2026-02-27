from .services import send_sms
from .models import SMSLog


def send_user_sms(user, text):
    sub = getattr(user, "active_sms_subscription", None)

    if not sub:
        return False

    # LIMIT CHECK
    if sub.sms_used >= sub.tariff.sms_limit:
        return False  # BAN

    status = send_sms(user.phone, text)

    if status:
        sub.sms_used += 1
        sub.save()

    SMSLog.objects.create(
        user=user,
        phone=user.phone,
        text=text,
        status=status
    )

    return status