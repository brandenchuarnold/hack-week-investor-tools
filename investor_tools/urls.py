from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static

from investor_tools.views import home

urlpatterns = [	
    url(r'', home)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)