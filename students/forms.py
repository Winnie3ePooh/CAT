from django.contrib.auth.models import User
from django import forms
from .models import *
from registration.forms import RegistrationForm
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin.widgets import AdminDateWidget
from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password','email','first_name','last_name')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = StudyGroup
        fields = ('groupName',)
        widgets = {
            'groupName': ModelSelect2Widget(
                            queryset=StudyGroup.objects.all(),
                            search_fields=['groupName__icontains']
                        ,attrs={'class': 'selectpicker'})
        }

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = StudyGroup
#         fields = ('groupName',)
#         widgets = {
#             'groupName': ModelSelect2MultipleWidget(
#                             queryset=StudyGroup.objects.all(),
#                             search_fields=['groupName__icontains']
#                         ,attrs={'class': 'selectpicker'})
#         }
