from django.conf.urls import url
from course_updates import views

urlpatterns = [
  url(r'^$', views.List.as_view(), name='list'),
]
