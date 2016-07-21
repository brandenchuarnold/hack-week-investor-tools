from django.conf.urls import patterns, url

from investor_tools.views import HomePageView

urlpatterns = patterns(
    '',

    url(r'', HomePageView.as_view(), name='home'),
)