"""
URLs for the CCX Feature.
"""
from django.conf.urls import patterns, url
from lms.djangoapps.ccx import views

urlpatterns = patterns(
    '',
    url(r'^ccx_coach$',
        'ccx.views.dashboard', name='ccx_coach_dashboard'),
    url(r'^edit_custom_course$',
        'ccx.views.edit_course_view', name='ccx_edit_course_view'),
    url(r'^create_ccx$',
        'ccx.views.create_ccx', name='create_ccx'),
    url(r'^edit_ccx$',
        'ccx.views.edit_ccx', name='edit_ccx'),
    url(r'^save_ccx$',
        'ccx.views.save_ccx', name='save_ccx'),
    url(r'^ccx_invite$',
        'ccx.views.ccx_invite', name='ccx_invite'),
    url(r'^ccx_schedule$',
        'ccx.views.ccx_schedule', name='ccx_schedule'),
    url(r'^ccx_manage_student$',
        'ccx.views.ccx_student_management', name='ccx_manage_student'),

    # Grade book
    url(r'^ccx_gradebook$',
        'ccx.views.ccx_gradebook', name='ccx_gradebook'),
    url(r'^ccx_gradebook/(?P<offset>[0-9]+)$',
        'ccx.views.ccx_gradebook', name='ccx_gradebook'),

    url(r'^ccx_grades.csv$',
        'ccx.views.ccx_grades_csv', name='ccx_grades_csv'),
    url(r'^ccx_set_grading_policy$',
        'ccx.views.set_grading_policy', name='ccx_set_grading_policy'),
    url(r'^ccx_messages/create/$', 'ccx.views.ccx_messages_create', name='ccx_messages_create'),
    url(r'^ccx_messages/delete/(?P<message_id>[^/]*)$', 'ccx.views.ccx_messages_delete', name='ccx_messages_delete'),
    url(r'^ccx_messages$', 'ccx.views.ccx_messages', name='ccx_messages'),
)
