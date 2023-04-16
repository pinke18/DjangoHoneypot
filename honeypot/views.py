from admin_honeypot.signals import honeypot
from django.dispatch import receiver
from admin_honeypot.models import LoginAttempt

# Create your views here.
from ipware import get_client_ip
import requests
import time

from honeypot.models import LoginAttemptExtended


@receiver(honeypot, sender=LoginAttempt)
def my_handler(sender, **kwargs):
    for key, value in kwargs.items():
        if key == "request":
            ip_address, is_routable = get_client_ip(value)
            response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
            time.sleep(1)
            instance = LoginAttemptExtended(
                username=value.POST.get('username'),
                password=value.POST.get('password'),
                country=response.get("country_name"),
                city=response.get("city"),
                session_key=value.session.session_key,
                ip_address=ip_address,
                user_agent=value.META.get('HTTP_USER_AGENT'),
                path=value.get_full_path(),
            )
            instance.save()
            #print(response.get("country_name"), response.get("city"))

