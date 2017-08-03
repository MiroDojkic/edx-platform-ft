from django.views.generic import ListView
from course_updates.models import CourseUpdates

class List(ListView):
  model=CourseUpdates
  template_name='course_updates/list.html'

