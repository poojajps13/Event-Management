from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('event/', include(('event.urls', 'event'), namespace='event')),
    path('account/', include(('account.urls', 'account'), namespace='account')),
    path('registration/', include(('registration.urls', 'registration'), namespace='registration')),

    re_path('froala_editor/', include('froala_editor.urls')),

    # path('set', set_user),
    path('VLSI_Design/', vlsi_design, name='vlsi_design'),
    path('Big_Data_Analytics/', big_data, name='big_data'),
    path('SMC_India_PvtLtd./', smc_india, name='smc_india'),
    path('Texas_Instruments_Embedded_System_Lab/', texas, name='texas'),
    path('ABES_NI_Innovation_Centre/', innovation_centre, name='innovation_centre'),
    path('Software_Development/', software_development, name='software_development'),
    path('Structural_Design_and_Analysis/', structural_design, name='structural_design'),
    path('Mobile_Application_Development/', mobile_application, name='mobile_application'),
    path('Cisco_Networking_Academy/', cisco_networking_academy, name='cisco_networking_academy'),
    path('Industrial_Automation_Research_&_Training_Centre_(IARTC)/', automation_research, name='automation_research'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
