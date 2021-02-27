from django.contrib import admin
from django.conf.urls import url,include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'', include('main.urls')),
    url(r'', include('users.urls')),
    url(r'', include('super_admin.urls')),
    url(r'', include('seller_admin.urls')),
    url(r'', include('customer.urls')),
    url(r'', include('frontEnd.urls')),
    url(r'', include('service.urls')),
    url(r'chat', include('core.urls')),
    url(r'', include('testapp.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
