from django.conf.urls import url, include
from django.contrib import admin
from registration.backends.simple.views import RegistrationView

class MyRegistrationView(RegistrationView):
        def get_success_url(self, request, user):
            return '/students/'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^students/', include('students.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^tests/', include('tests.urls')),
]
