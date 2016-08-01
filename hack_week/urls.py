from django.conf.urls import * 

urlpatterns = patterns(
    '',

    url(r'', include('investor_tools.urls')),
)
