
from django import template
from frontend.models import SchoolInfo  # Import your SchoolInfo model

register = template.Library()

@register.simple_tag
def get_school_info():
    return SchoolInfo.objects.all()
