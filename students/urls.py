from django.conf.urls import url
from registration.backends.default.views import RegistrationView
from .forms import *

from . import views
app_name='students'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^details/$', views.details, name='details'),
    url(r'^allUsers/$', views.allUsers, name='allUsers'),
    url(r'^register/$', views.register, name='register'), # ADD NEW PATTERN!
]
