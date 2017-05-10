from django.db import models
import random
from django.contrib.auth.models import User


def randomCompl():
    return random.uniform(1,100)

class Discipline(models.Model):
    disciplineName = models.CharField(max_length=200)

class Subject(models.Model):
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE,null=True,blank=True)
    subjectName = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=0)
    def __str__(self):
        return self.subjectName

class TestSettings(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    publicResults = models.BooleanField(default=False)

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
    name = models.CharField(max_length=200, default='')
    filePath = models.CharField(max_length=100, default='')
    rightAnswers = models.IntegerField(default=0)
    wrongAnswers = models.IntegerField(default=0)
    isVisible = models.BooleanField(default=True)
