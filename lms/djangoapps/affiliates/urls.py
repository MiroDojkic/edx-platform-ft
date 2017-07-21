"""
URLs for the Affiliate Feature.
"""
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'affiliates.views.index', name='affiliates_index'),
    url(r'^new$', 'affiliates.views.create', name='affiliate_create'),
    url(r'^(?P<pk>[^/]*)$', 'affiliates.views.show', name="affiliate_show"),
    url(r'^edit/(?P<pk>\d+)$', 'affiliates.views.edit', name='affiliate_edit'),
)
