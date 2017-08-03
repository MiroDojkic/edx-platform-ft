from django.db import models
from django.contrib.auth.models import User
from lms.djangoapps.ccx.models import CustomCourseForEdX

class CourseUpdates(models.Model):
  date = models.DateField(blank=False, null=False)
  content = models.TextField(blank=False, null=False)
  author = models.ForeignKey(User)
  ccx = models.ForeignKey(CustomCourseForEdX)
