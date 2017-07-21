"""
URLs for the Affiliate Feature.
"""
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'affiliates.views.index', name='affiliates_index'),
    url(r'^new$', 'affiliates.views.new', name='affiliates_new'),
    url(r'^create$', 'affiliates.views.create', name='affiliates_create'),
    url(r'^(?P<pk>[^/]*)$', 'affiliates.views.show', name="affiliates_show"),
    url(r'^edit/(?P<pk>\d+)$', 'affiliates.views.edit', name='affiliates_edit'),
)
