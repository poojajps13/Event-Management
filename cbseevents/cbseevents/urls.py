from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include

from account.views import *
from events.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('event/', include(('event.urls', 'event'), namespace='event')),
    path('registration/', include(('registration.urls', 'registration'), namespace='registration')),
    path('superuser/', login_required(superuser), name='superuser'),
    path('login', Login.as_view(), name='login'),
    path('signup', Signup.as_view(), name='signup'),
    path('logout', login_required(logout), name='logout'),
    path('pdf', some_view, name='pdf'),
    path('account/activate/<uidb64>/<token>/', activate, name='activate'),
    path('account/forget-password/<uidb64>/<token>',ResetPassword.as_view(), name='forget-password'),
    path('edit_user/<username>', login_required(edit_user), name='edit_user'),
    path('consolidated/<username>', login_required(consolidated), name='consolidated'),
    path('consolidatedview/', login_required(consolidatedview), name='consolidatedview'),
    path('deleteuser/<username>', login_required(del_user), name='deleteuser'),
    path('Centre_of_Excellence_for_Structural_Design_and_Analysis/', structural_design, name='structural_design'),
    path('Cisco_Networking_Academy/', cisco_networking_academy, name='cisco_networking_academy'),
    path('Texas_Instruments_Embedded_System_Lab/', texas, name='texas'),
    path('Centre_of_Excellence_for_SMC_India_PvtLtd./', smc_india, name='smc_india'),
    path('Industrial_Automation_Research_&_Training_Centre_(IARTC)/', automation_research, name='automation_research'),
    path('Centre_of_Excellence_VLSI_Design/', vlsi_design, name='vlsi_design'),
    path('Center_of_Excellence_for_Big_Data_Analytics/', big_data, name='big_data'),
    path('ABES_NI_Innovation_Centre/', innovation_centre, name='innovation_centre'),
    path('Centre_of_Excellence_for_Mobile_Application_Development/', mobile_application, name='mobile_application'),
    path('Center_for_Enterprise_Software_Development/', software_development, name='software_development'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)