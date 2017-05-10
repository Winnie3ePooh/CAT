from django.contrib import admin

from tests.models import *
from tests.models import Theme

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Вопрос',               {'fields': ['theme','questionName','complexity','right','wrong']}),
    ]
    inlines = [AnswerInline]
admin.site.register(Discipline)
admin.site.register(Subject)
admin.site.register(Theme)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Result)
