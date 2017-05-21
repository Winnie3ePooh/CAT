from registration.backends.default.views import RegistrationView
from .forms import *
from .models import *


class MyRegistrationView(RegistrationView):

    form_class = UserForm

    def register(self, form_class):
        new_user = super(MyRegistrationView, self).register(form_class)
        p = form_class.cleaned_data['groupName']
        new_profile = UserProfile.objects.create(user=new_user, studygroup=p)
        new_profile.save()
        return new_user
