# middleware to log general requests and user activities.
from .models import Event
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
import os

# Event logging
class EventTrackingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            event_type = self.determine_event_type(request)
            Event.objects.create(
                user=request.user,
                event_type=event_type,
                path=request.path,
                method=request.method,
                additional_info=self.get_additional_info(request)
            )

    def determine_event_type(self, request):
        if request.method == 'POST':
            if 'create' in request.path:
                return 'create'
            elif 'update' in request.path:
                return 'update'
            elif 'delete' in request.path:
                return 'delete'
        elif request.method == 'GET':
            return 'view'
        return 'access'

    def get_additional_info(self, request):
        # Customize this to extract and log additional info as needed
        return None

# middleware to check for the secret key
class RestrictRegisterBySecretMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        secret_key = os.getenv('REGISTER_SECRET_KEY', 'default-secret-key')
        if request.path == '/register/' and request.GET.get('secret_key') != secret_key:
            return HttpResponseForbidden("You are not authorized to view this page.")
        response = self.get_response(request)
        return response
    