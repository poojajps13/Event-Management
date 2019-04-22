from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from .views import *

admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('event/', include(('event.urls', 'event'), namespace='event')),
    path('account/', include(('account.urls', 'account'), namespace='account')),
    path('registration/', include(('registration.urls', 'registration'), namespace='registration')),

    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),

    # path('set', set_user),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
