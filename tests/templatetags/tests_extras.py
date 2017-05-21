from django import template
from django.contrib.auth.models import Group, User
from django.db.models import Q
from students.models import *

register = template.Library()

@register.filter(name='available')
def availableTests(tests,user):
    group = StudyGroup.objects.get(groupName='All')
    return tests.filter(Q(studygroup=user.userprofile.studygroup) | Q(studygroup=group))

@register.filter(name='checkNotNull')
def checkNotNull(discs,user):
    group = StudyGroup.objects.get(groupName='All')
    return discs.distinct().filter(Q(subject__studygroup=user.userprofile.studygroup) | Q(subject__studygroup=group))
