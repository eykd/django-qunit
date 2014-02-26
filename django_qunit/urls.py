from django.conf.urls import patterns, url
from django.conf import settings
import os

static_root = os.path.join(os.path.dirname(__file__), 'static')

urlpatterns = patterns('',
    url(r'^tests/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.QUNIT_TEST_DIRECTORY,
    }, name='qunit_test'),
    url(r'^qunit/qunit.js', 'django.views.static.serve', {
        'document_root': static_root, 'path': 'qunit/qunit.js',
    }, name='qunit_js'),
    url(r'^qunit/qunit.css', 'django.views.static.serve', {
        'document_root': static_root, 'path': 'qunit/qunit.css',
    }, name='qunit_css'),
    url('^(?P<path>.*)$', 'django_qunit.views.run_tests',
        name='qunit_test_overview'),
)
