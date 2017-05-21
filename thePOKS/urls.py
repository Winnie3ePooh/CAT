from django.conf.urls import url, include
from django.contrib import admin
from registration.backends.simple.views import RegistrationView
from students.forms import *
from students.regbackend import MyRegistrationView

# class MyRegistrationView(RegistrationView):
#         def get_success_url(self, request, user):
#             return '/'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('students.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^tests/', include('tests.urls')),
    url(r'^select2/', include('django_select2.urls')),
]
