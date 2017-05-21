from django import forms
from tests.models import *
from students.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_select2.forms import (
    HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget,
    ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget,
    Select2Widget
)

class UploadFileForm(forms.Form):
    title = forms.CharField(
        label = "Желаемое название:",
        max_length=50,
        required = False,
    )

    CHOICES = ((True, 'Да',), (False, 'Нет',))
    publicResults = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    file = forms.FileField(
        label = "Выберите файл",
        required=True
    )

class StudyGroupsForm(forms.ModelForm):
    class Meta:
        model = StudyGroup
        fields = ('groupName',)
        widgets = {
            'groupName': ModelSelect2MultipleWidget(
                            queryset=StudyGroup.objects.all(),
                            search_fields=['groupName__icontains']
                        )
        }

class ChoosingGroupForm(forms.Form):
    group = forms.ModelChoiceField(
        queryset=StudyGroup.objects.all(),
        label='Группа',
        widget=ModelSelect2Widget(
            model=StudyGroup,
            search_fields=['groupName__icontains']
        )
    )

    def __init__(self, *args, **kwargs):
        group = kwargs.pop('groupName', None)
        super(ChoosingGroupForm, self).__init__(*args, **kwargs)

        if group:
            self.fields['group'].queryset = StudyGroup.objects.filter(groupName__in=group)

class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.get_full_name()

class ChoosingStudentForm(forms.Form):
    students = UserModelChoiceField(
        queryset=User.objects.all(),
        label='Студент',
        widget=ModelSelect2Widget(
            model=User,
            search_fields=['first_name__icontains','last_name__icontains']
        )
    )

    def __init__(self, *args, **kwargs):
        group = kwargs.pop('groupName', None)
        super(ChoosingStudentForm, self).__init__(*args, **kwargs)

        if group:
            self.fields['students'].queryset = User.objects.distinct().filter(userprofile__studygroup__groupName__in=group)


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['theme','questionName']
        labels = {
            'theme': _('Тема'),
            'questionName': _('Вопрос'),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answerText','isRight']
        labels = {
            'answerText': _('Ответ'),
            'isRight': _('Правильный'),
        }
