from django import forms
from tests.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from django.utils.translation import ugettext_lazy as _

class UploadFileForm(forms.Form):
    title = forms.CharField(
        label = "Желаемое название:",
        max_length=50,
        required = False,
    )
    CHOICES=((True,'Да'),
                (False,'Нет'))
    is_visible = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        initial='True',
        required=True
    )
    file = forms.FileField(
        label = "Выберите файл",
        required=True
    )
    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.add_input(Submit('submit', 'Загрузить',onclick="$('#myPleaseWait').modal('show');"))

class QuestionForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(QuestionForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper(self)
    #     self.helper.form_tag = False
    #     self.helper.form_class = 'form-horizontal'
    #     self.helper.label_class = 'col-lg-3'
    #     self.helper.field_class = 'col-lg-8'
    #     self.helper.layout = Layout(
    #         'Вопрос',
    #         'theme',
    #         'questionName',
    #         'qType'
    #     )

    class Meta:
        model = Question
        fields = ['theme','questionName']
        labels = {
            'theme': _('Тема'),
            'questionName': _('Вопрос'),
        }

class AnswerForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(AnswerForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper(self)
    #     self.helper.form_tag = False
    #     self.helper.form_class = 'form-horizontal'
    #     self.helper.label_class = 'col-lg-3'
    #     self.helper.field_class = 'col-lg-8'

    class Meta:
        model = Answer
        fields = ['answerText','isRight']
        labels = {
            'answerText': _('Ответ'),
            'isRight': _('Правильный'),
        }
