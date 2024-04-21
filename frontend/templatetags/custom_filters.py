from django import template
from frontend.models import Teachers

register = template.Library()

@register.filter
def get_teacher_name(teacher_id):
    try:
        teacher = Teachers.objects.get(teacherid=teacher_id)
        return teacher.teachername
    except Teachers.DoesNotExist:
        return "Unknown Teacher"
