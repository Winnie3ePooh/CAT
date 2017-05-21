# coding: utf8
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from tests import nbc
from tests import writeTest as wt
from django.conf import settings
from .forms import *
from django.forms import *
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from tests.models import *
from django.views.decorators.csrf import csrf_protect


import xml.etree.ElementTree as ET
import numpy as np
import json
import random
import glob, os
import math

DIFF = {
    'Easy': [0.8,1],
    'EasyMedium': [0.65,0.8],
    'Medium': [0.4,0.65],
    'MediumHard': [0.2,0.4],
    'Hard':[0,0.2]
}

class IndexView(generic.ListView):
    template_name = 'tests/index.html'
    context_object_name = 'all_disciplines'

    def get_queryset(self):
        return Discipline.objects.order_by('disciplineName')


def usersTests(request):
    results = Result.objects.all().filter(user=request.user)
    return render(request, 'tests/resultsView.html', {'results': results})

def resultDetails(request, resultsID):
    result = Result.objects.get(pk=resultsID)
    return render(request, 'tests/resultDetails.html', {'result': result})

def detailedReport(request, resultsID):
    result = Result.objects.get(pk=resultsID)
    with open(os.path.join(settings.MEDIA_ROOT,result.filePath)) as f:
        data = json.load(f)
    return render(request, 'tests/detailedReport.html', {'data': data['Answers']})


def setInitialParams(request, subjectID):
    path = os.path.join(settings.MEDIA_ROOT,str(request.user))
    request.session['filePath'] = path+str(len(glob.glob(path+'*.json')))+'.json'
    with open(request.session['filePath'],'x') as f:
        f.write('{"Answers":[],"Bayes":[]}')
    request.session['flag'] = False
    request.session['calib'] = False
    request.session['subjectID'] = subjectID
    return HttpResponseRedirect(reverse('tests:startTesting'))


def startTesting(request):
    if not request.session['calib']:
        subjectID = request.session['subjectID']
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
        request.session['score'] = 0
        request.session['testName'] = currSubject.subjectName
        request.session['lvl'] = 0
        request.session['checking'] = True
        for item in themeID:
            request.session['calibQuest'].extend(Question.objects.filter(theme_id= item, complexity__range=DIFF['Medium']).values_list('id',flat=True).order_by('?')[:3])
        #request.session['calibQuest'] = list(Question.objects.all().values_list('id',flat=True))
    if request.session['calibQuest']:
        listCopy = request.session['calibQuest']
        questionID = listCopy.pop()
        #request.session['exclude'].append({questionID:''})
        request.session['calibQuest'] = listCopy
        question = Question.objects.get(pk=questionID)
        return render(request, 'tests/test.html', {'question': question})
    else:
        request.session['calibStatistic'] = request.session['testStatistic']['Results']
        request.session['calib'] = False
        return HttpResponseRedirect(reverse('tests:getNextQuestion'))

def getNextQuestion(request):
    checking = nbc.setNextDiff(request)
    print('OLOLO {} {}'.format(checking,request.session['lvl']))
    print(len(request.session['excludeID']))
    print('БАЛЛЫ {}'.format(request.session['score']/len(request.session['excludeID'])))
    score = 10*request.session['score']/len(request.session['excludeID'])
    #print(math.fabs((request.session['lvl']-checking)))
    if  0.2 <= checking <= 0.6 and math.fabs(checking-request.session['lvl']) >= 0.01:
        request.session['lvl'] = checking
        themeID = str(request.session['themeID'].pop())
        cmpl = DIFF[request.session['testStatistic']['Themes'][themeID]['currDiff']]
        # for item in request.session['themeID']:
        #     diff = request.session['testStatistic']["Themes"][str(item)]["currDiff"]
        #     request.session['calibQuest'].extend(Question.objects.filter(theme_id= item, complexity__range=DIFF[diff]).values_list('id',flat=True).order_by('?')[:1])
        # request.session['calib'] = True
        # subjectID = request.session.get('subjectID')
        # return HttpResponseRedirect(reverse('tests:startTesting',args=(subjectID,)))
        question = Question.objects.filter(theme_id = themeID, complexity__range = cmpl).exclude(pk__in = request.session['excludeID']).values().order_by('?')[:1]
        request.session['themeID'].insert(0,themeID)
        if question:
            question = Question.objects.get(pk=question[0]['id'])
            return render(request, 'tests/test.html', {'question': question})
        else:
            return HttpResponseRedirect(reverse('tests:getNextQuestion'))
    else:
        testsStatistics, flag = TestsStatistic.objects.get_or_create(subject_id=request.session['subjectID'])
        testsStatistics.all += 1
        isPassed = False
        endFlag = 'ЗАГЛУШКА'
        if checking >= 0.6:
            endFlag = 'Достигнут нужный уровень'
            isPassed = True
            testsStatistics.passed += 1
        elif checking <= 0.2:
            endFlag = 'Ну вообще'
            isPassed = False
        res = request.session['testStatistic']['Results']
        result = Result(user=request.user,
                        subject=Subject.objects.get(pk=request.session['subjectID']),
                        filePath=request.session['filePath'].split('\\')[-1],
                        rightAnswers=res['right'],wrongAnswers=res['wrong'],
                        score=score,
                        isPassed=isPassed)
        result.save()
        return render(request, 'tests/results.html',{'results': result,'main': request.session['mainStatistic']['Results'],'calib':request.session['calibStatistic'],'endFlag':endFlag})

def studentAnswer(request, themeID, questionID):
    request.POST = request.POST.copy()
    if request.method == 'POST':
        try:
            studAnswer = request.POST.pop('answer')
            studAnswer = [int(s) for s in studAnswer]
        except KeyError:
            studAnswer = ['']
        check = False
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
        pj = currQuestion.right/(currQuestion.right+currQuestion.wrong)
        #request.session['exclude'][-1][currQuestion.id] = math.log((1-pj)/pj)
        request.session['exclude'].append({currQuestion.id:math.log((1-pj)/pj)})
        request.session['excludeID'].append(questionID)
        currQuestion.save()
        if check:
            #request.session['score'] += 4*(100-round(float(cmplty)))/100
            request.session['score'] +=1
            request.session['mainStatistic']['Results']['right'] += 1
        else:
            request.session['mainStatistic']['Results']['wrong'] += 1
        if request.session['calib']:
            return HttpResponseRedirect(reverse('tests:startTesting'))
        else:
            return HttpResponseRedirect(reverse('tests:getNextQuestion'))

def uploadFile(request):
    if request.method == 'POST':
        uploadForm = UploadFileForm(request.POST, request.FILES)
        if uploadForm.is_valid():
            try:
                os.mkdir(os.path.join(settings.MEDIA_ROOT, request.user.username))
            except:
                pass
            currPath = os.path.join(settings.MEDIA_ROOT, request.user.username,request.FILES['file'].name)
            with open(currPath, 'wb+') as destination:
                for chunk in request.FILES['file'].chunks():
                    destination.write(chunk)
            processingTestsFile(currPath,request,uploadForm)
            return HttpResponseRedirect('/')
    else:
        uploadForm = UploadFileForm()
        groups = StudyGroupsForm()
        groups = render_to_string('picker.html',{'form':groups},request)
    return render(request, 'tests/upload.html', {'uploadForm': uploadForm,'groups':groups})

def myTests(request):
    user_tests = Subject.objects.all().filter(user=request.user).order_by('subjectName')
    paginator = Paginator(user_tests, 10) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        userTests = paginator.page(page)
    except PageNotAnInteger:
        userTests = paginator.page(1)
    except EmptyPage:
        userTests = paginator.page(paginator.num_pages)
    return render(request, 'tests/myTests.html', {'userTests': userTests})

def testDetails(request, testID):
    request.session['testID'] = testID
    subject = Subject.objects.get(pk=testID)
    themesIDs = subject.theme_set.all()
    testsQuestions = Question.objects.all().filter(theme__in=themesIDs).order_by('theme')
    paginator = Paginator(testsQuestions, 10) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)
    return render(request, 'tests/testDetails.html', {'questions': questions})

def groupsTestDetails(request, testID=None):
    print('ЗАШЁЛ')
    subj = Subject.objects.get(pk=testID).studygroup.all().values_list('groupName')
    print(subj)
    if request.method == 'POST':
        group = request.POST['group']
        results = Result.objects.filter(subject__studygroup__groupName=group)
        data = {
            'group': group,
            'total': results.count(),
            'right': results.filter(isPassed=True).count(),
            'results': results
        }
        return HttpResponse(render_to_string('tests/testGroupStats.html',{'data':data},request))
    form = ChoosingGroupForm(groupName=subj)
    return render(request,'picker.html',{'form':form,'flag':'group'})

def usersTestDetails(request, testID):
    print('ЗАШЁЛ')
    print(User.objects.all())
    subj = Subject.objects.get(pk=testID).studygroup.all().values_list('groupName')
    print(subj)
    if request.method == 'POST':
        group = request.POST['group']
        group = group.split(' ')
        print(group)
        results = Result.objects.filter(user__first_name=group[0],user__last_name=group[1])
        data = {
            'group': group,
            'total': results.count(),
            'right': results.filter(isPassed=True).count(),
            'results': results
        }
        return HttpResponse(render_to_string('tests/testGroupStats.html',{'data':data},request))
    form = ChoosingStudentForm(groupName=subj)
    return render(request,'picker.html',{'form':form,'flag':'user'})

def deleteTest(request):
    if request.method == 'GET':
        print(request.GET['test_id'])
        subject = Subject.objects.get(pk=request.GET['test_id'])
        subject.delete()
        data = {
            'rdy': True
        }
        return JsonResponse(data)

def questionCreate(request):

    question = Question()
    answersFormSet = inlineformset_factory(Question,Answer, form=AnswerForm,extra=5, can_delete=True)

    if request.method == 'POST':
        tuf = QuestionForm(request.POST, request.FILES,instance=question, prefix="main")
        formset = answersFormSet(request.POST, request.FILES, instance=question, prefix="nested")
        if tuf.is_valid() and formset.is_valid():
            tuf.save()
            formset.save()
            return HttpResponseRedirect(reverse('tests:testDetails',args=(request.session['testID'],)))
        else:
            return HttpResponse(404)
    else:
        tuf = QuestionForm(instance=question, prefix="main")
        formset = answersFormSet(instance=question,prefix="nested")
        form  = render_to_string('tests/modalCreate.html',{'question':tuf,'answers':formset},request)

    return HttpResponse(form)

def questionEdit(request):
    if not request.method=='POST':
        try:
            del request.session['questionID']
        except KeyError:
            pass
    try:
        questionID = request.session['questionID']
    except KeyError:
        questionID = request.GET['questionID']

    question = get_object_or_404(Question, pk=int(questionID))
    answersFormSet = inlineformset_factory(Question,Answer, form=AnswerForm,extra=4, can_delete=True)
    if request.method == 'POST':
        tuf = QuestionForm(request.POST, request.FILES,instance=question, prefix="main")
        formset = answersFormSet(request.POST, request.FILES, instance=question, prefix="nested")
        if tuf.is_valid() and formset.is_valid():
            tuf.save()
            formset.save()
            return HttpResponseRedirect(reverse('tests:testDetails',args=(request.session['testID'],)))
        else:
            return HttpResponse(404)
    else:
        tuf = QuestionForm(instance=question, prefix="main")
        formset = answersFormSet(instance=question,prefix="nested")
        form  = render_to_string('tests/modalUpdate.html',{'question':tuf,'answers':formset},request)
        request.session['questionID'] = request.GET['questionID']

    return HttpResponse(form)

def questionDelete(request):
    questionID = request.GET['questionID']
    question = get_object_or_404(Question, pk=int(questionID))
    question.delete()
    data = {
        'rdy': True
    }
    return JsonResponse(data)

def processingTestsFile(fPath,request,uploadForm):
    themes=[]
    root = ET.parse(fPath).getroot()
    disc = root.find('category')
    try:
        print('OLOLO RABOTAET')
        discipline = Discipline.objects.get(disciplineName=disc.text)
    except Discipline.DoesNotExist:
        discipline = Discipline(disciplineName=disc.text)
        discipline.save()
    for name in root.iter('name'):
        print(request.POST)
        subj = Subject(discipline=discipline,
                       subjectName=name.text,
                       user=request.user,
                       publicResults=request.POST['publicResults'])
        subj.save()
        for item in request.POST.getlist('groupName'):
            subj.studygroup.add(item)

    for child in root.iter('theme'):
        theme = Theme(themeName=child.text, subject=subj)
        theme.save()
        themes.append(theme)

    for child in root.iter('question'):
        quest = Question(questionName=child[0].text, theme=themes[int(child.get('theme'))])
        quest.save()
        for ans in child[1].iter('answer'):
            if ans.get('isCorrect') == '1':
                answer = Answer(answerText=ans.text, isRight = True, question=quest)
            else:
                answer = Answer(answerText=ans.text, isRight = False, question=quest)
            answer.save()
    return subj
