from django.conf.urls import patterns, url

from investor_tools.views import home

urlpatterns = patterns(
    '',

    url(r'', home),
)