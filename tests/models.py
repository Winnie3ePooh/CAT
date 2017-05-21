from django.db import models
import random
from django.contrib.auth.models import User
from students.models import *


def randomCompl():
    return random.uniform(1,100)

class Discipline(models.Model):
    disciplineName = models.CharField(max_length=200)

class Subject(models.Model):
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE,null=True,blank=True)
    subjectName = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=0)
    studygroup = models.ManyToManyField(StudyGroup,related_name='groups')
    publicResults = models.BooleanField(default=False)
    def __str__(self):
        return self.subjectName

class TestsStatistic(models.Model):
    subject = models.OneToOneField(Subject)
    passed = models.IntegerField(default=0)
    all = models.IntegerField(default=0)

class Theme(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    themeName = models.CharField(max_length=200)
    def __str__(self):
        return self.themeName

class Question(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    questionName = models.CharField(max_length=200)
    complexity = models.FloatField(default=randomCompl)
    qType = models.CharField(max_length=10)
    right = models.IntegerField(default=0)
    wrong = models.IntegerField(default=0)
    def __str__(self):
        return self.questionName

    def getRightAnswersCount(self):
        if self.qType == 'Один':
            return True
        else:
            return False

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answerText = models.CharField(max_length=200)
    isRight = models.BooleanField()
    def __str__(self):
        return self.answerText

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject)
    filePath = models.CharField(max_length=100, default='')
    rightAnswers = models.IntegerField(default=0)
    wrongAnswers = models.IntegerField(default=0)
    score = models.FloatField(default=0)
    isPassed = models.BooleanField(default=True)
