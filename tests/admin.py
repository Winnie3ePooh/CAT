from django.contrib import admin

from tests.models import Subject, Question, Answer, Resutl
from tests.models import Theme

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Вопрос',               {'fields': ['theme','questionName','complexity']}),
    ]
    inlines = [AnswerInline]

admin.site.register(Subject)
admin.site.register(Theme)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Resutl)