from django import template
import datetime
# from frontend.models import Teachers

register = template.Library()

# @register.filter
# def get_teacher_name(teacher_id):
#     try:
#         teacher = Teachers.objects.get(teacherid=teacher_id)
#         return teacher.teachername
#     except Teachers.DoesNotExist:
#         return "Unknown Teacher"


# to add specified number of hours to a date object
@register.filter
def add_hours(value, hours):
    if isinstance(value, datetime.datetime):
        return value + datetime.timedelta(hours=hours)
    return value