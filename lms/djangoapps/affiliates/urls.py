"""
URLs for the Affiliate Feature.
"""
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'affiliates.views.index', name='index'),
    url(r'^new$', 'affiliates.views.new', name='new'),
    url(r'^create$', 'affiliates.views.create', name='create'),
    url(r'^(?P<pk>[^/]*)$', 'affiliates.views.show', name="show"),
    url(r'^edit/(?P<pk>\d+)$', 'affiliates.views.edit', name='edit'),
    url(r'^add_member/(?P<pk>\d+)$', 'affiliates.views.add_member', name='add_member'),
    url(r'^remove_member/(?P<pk>\d+)$', 'affiliates.views.remove_member', name='remove_member'),
)
