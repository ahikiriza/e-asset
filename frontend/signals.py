# frontend/signals.py
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import Event

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    Event.objects.create(
        user=user,
        event_type='login',
        path=request.path,
        method=request.method,
        additional_info='User logged in'
    )

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    Event.objects.create(
        user=user,
        event_type='logout',
        path=request.path,
        method=request.method,
        additional_info='User logged out'
    )