from django.db import models
from django.contrib.auth.models import User

class StudyGroup(models.Model):
    groupName = models.CharField(max_length=6)

    def __str__(self):
        return self.groupName


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    birthDate = models.DateField(auto_now_add=True)
    studygroup = models.ForeignKey(StudyGroup,on_delete=None,default=0)

def getFullName(self):
    return self.get_full_name()

User.add_to_class("__str__", getFullName)
