# coding: utf8
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from tests import nbc
from tests import writeTest as wt
from django.conf import settings
from .forms import UploadFileForm

import xml.etree.ElementTree as ET
import numpy as np
import json
import random
import glob, os
import math

from tests.models import Subject, Question, Answer, Theme, Resutl

DIFF = {
    'Easy': [80,100],
    'EasyMedium': [60,80],
    'Medium': [40,60],
    'MediumHard': [20,40],
    'Hard':[0,20]
}

class IndexView(generic.ListView):
    template_name = 'tests/index.html'
    context_object_name = 'all_subjects'

    def get_queryset(self):
        return Subject.objects.order_by('subjectName')

def usersTests(request):
    results = Resutl.objects.all().filter(user=request.user)
    return render(request, 'tests/resultsView.html', {'results': results})

def testDetails(request, resultsID):
    result = Resutl.objects.get(pk=resultsID)
    return render(request, 'tests/testDetails.html', {'result': result})

def detailedReport(request, resultsID):
    result = Resutl.objects.get(pk=resultsID)
    with open(os.path.join(settings.MEDIA_ROOT,result.filePath)) as f:
        data = json.load(f)
    return render(request, 'tests/detailedReport.html', {'data': data})


def detailView(request, subjectID):
    path = os.path.join(settings.MEDIA_ROOT,str(request.user))
    request.session['filePath'] = path+str(len(glob.glob(path+'*.json')))+'.json'
    with open(request.session['filePath'],'x') as f:
        f.write('{"Answers":[]}')
    request.session['flag'] = False
    request.session['calib'] = False
    request.session['subjectID'] = subjectID
    return HttpResponseRedirect(reverse('tests:startTesting', args=(subjectID,)))


def startTesting(request, subjectID):
    if not request.session['calib']:
        currSubject  = Subject.objects.get(pk=subjectID)
        themeID = list(currSubject.theme_set.all().values_list('id',flat=True))
        testStatistic = {'Results': {'right': 0, 'wrong': 0},'Themes':{}}
        for item in themeID:
            testStatistic['Themes'][item] = {'currDiff': 'Medium', 'rightAnswers': 0, 'wrongAnswers': 0,
                                   'normalizedValue': 0}
        request.session['testStatistic'] = testStatistic
        request.session['mainStatistic'] = {'Results': {'right': 0, 'wrong': 0}}
        request.session['calib'] = True
        request.session['themeID'] = themeID
        request.session['calibQuest'] = []
        request.session['exclude'] = []
        request.session['excludeID'] = []
        request.session['checkEnd'] = 0
        request.session['testName'] = currSubject.subjectName
        for item in themeID:
            request.session['calibQuest'].extend(list(Question.objects.filter(theme_id= item, complexity__range=DIFF['Medium']).values_list('id',flat=True).order_by('?')[:2]))
        #request.session['calibQuest'] = list(Question.objects.all().values_list('id',flat=True))
        request.session['score'] = 0
    if request.session['calibQuest']:
        listCopy = request.session['calibQuest']
        questionID = listCopy.pop()
        request.session['exclude'].append({questionID:''})
        request.session['excludeID'].append(questionID)
        print(request.session['exclude'])
        request.session['calibQuest'] = listCopy
        question = Question.objects.get(pk=questionID)
        return render(request, 'tests/test.html', {'question': question})
    else:
        request.session['calibStatistic'] = request.session['testStatistic']['Results']
        request.session['calib'] = False
        return HttpResponseRedirect(reverse('tests:getNextQuestion'))

def getNextQuestion(request):
    check = nbc.setNextDiff(request.session['testStatistic'],request)
    if check >= 0.3 and request.session['checkEnd'] != 5:
        themeID = str(random.choice(request.session['themeID']))
        cmpl = DIFF[request.session['testStatistic']['Themes'][themeID]['currDiff']]
        question = Question.objects.filter(theme_id = themeID, complexity__range = cmpl).exclude(pk__in = request.session['excludeID']).values()[:1]
        if question:
            question = Question.objects.get(pk=question[0]['id'])
            return render(request, 'tests/test.html', {'question': question})
        else:
            return HttpResponseRedirect(reverse('tests:getNextQuestion'))
    else:
        if check <= 0.3:
            endFlag = 'Превышен порог минимального балла'
        else:
            endFlag = 'Допущено 5 подряд ошибок'
        res = request.session['testStatistic']['Results']
        result = Resutl(user=request.user,name=request.session['testName'],
                        filePath=request.session['filePath'].split('\\')[-1],
                        rightAnswers=res['right'],wrongAnswers=res['wrong'],
                        calibRight=request.session['calibStatistic']['right'],calibWrong=request.session['calibStatistic']['wrong'],
                        mainRight=request.session['mainStatistic']['Results']['right'],mainWrong=request.session['mainStatistic']['Results']['wrong'],
                        score=res['right']+res['wrong'])
        result.save()
        return render(request, 'tests/results.html',{'results': result,'main': request.session['mainStatistic']['Results'],'calib':request.session['calibStatistic'],'endFlag':endFlag})

def studentAnswer(request, themeID, questionID, cmplty):
    request.POST = request.POST.copy()
    studAnswer = request.POST.pop('answer')
    studAnswer = [int(s) for s in studAnswer]
    check = False
    if request.method == 'POST':
        currQuestion = Question.objects.get(pk=questionID)
        rightAnswers = list(currQuestion.answer_set.all().filter(isRight = True).values_list('id',flat=True).order_by('?'))
        wt.writeAnswers(request,currQuestion,studAnswer,rightAnswers)
        subjectID = request.session.get('subjectID')
        if set(rightAnswers) == set(studAnswer):
            request.session['testStatistic'] = nbc.updateValues(request.session['testStatistic'],themeID,True)
            check = True
            currQuestion.right += 1
        else:
            request.session['testStatistic'] = nbc.updateValues(request.session['testStatistic'],themeID,False)
            currQuestion.wrong += 1
        currQuestion.save()
        pj = currQuestion.right/(currQuestion.right+currQuestion.wrong)
        request.session['exclude'][-1][currQuestion.id] = math.log((1-pj)/pj)
        if request.session['calib']:
            return HttpResponseRedirect(reverse('tests:startTesting',args=(subjectID,)))
        else:
            if check:
                request.session['score'] += 4*(100-round(float(cmplty)))/100
                request.session['checkEnd'] = 0
                request.session['mainStatistic']['Results']['right'] += 1
            else:
                request.session['checkEnd'] += 1
                request.session['mainStatistic']['Results']['wrong'] += 1
            return HttpResponseRedirect(reverse('tests:getNextQuestion'))

def uploadFile(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print(request.FILES['file'])
            #handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/students/')
    else:
        form = UploadFileForm()
    return render(request, 'tests/upload.html', {'form': form})
