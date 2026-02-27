import requests
from django.conf import settings


def send_sms(phone: str, text: str) -> bool:
    try:
        res = requests.post(
            settings.SMS_GATEWAY_URL,
            json={
                "phone": phone,
                "text": text
            },
            timeout=5
        )

        return res.status_code == 200

    except Exception:
        return False
