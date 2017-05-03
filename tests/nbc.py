import numpy as np
import json
import glob, os
import math

from django.conf import settings
from tests.models import Question, Answer

DIFFICULTIES = (
    ("Easy",(80,100)),
    ("EasyMedium",(60,80)),
    ("Medium",(40,60)),
    ("MediumHard",(20,40)),
    ("Hard",(0,20))
)
NORMILIZED = {
    'Easy':{
        'Easy':(0,0.33),
        'EasyMedium':(0.33,0.66),
        'Medium': (0.66,1)
    },
    'EasyMedium':{
        'Easy':(0,0.25),
        'EasyMedium':(0.25,0.5),
        'Medium': (0.5,0.75),
        'MediumHard': (0.75,1),
    },
    'Medium':{
        'Easy':(0,0.2),
        'EasyMedium':(0.2,0.4),
        'Medium':( 0.4,0.6),
        'MediumHard': (0.6,0.8),
        'Hard': (0.8,1)
    },
    'MediumHard':{
        'EasyMedium':(0,0.25),
        'Medium': (0.25,0.5),
        'MediumHard': (0.5,0.75),
        'Hard': (0.75,1)
    },
    'Hard':{
        'Medium':(0,0.33),
        'MediumHard':(0.33,0.66),
        'Hard': (0.66,1)
    }
}

def getNextDiff(curr,currDif):
    for value in NORMILIZED[currDif].items():
        if (curr >= value[-1][0]) and (curr <= value[-1][1]):
            return value[0]

def updateValues(data,themeID,checkVal):
    if checkVal:
        data["Themes"][themeID]["rightAnswers"] += 1
        data["Results"]["right"] += 1
    else:
        data["Themes"][themeID]["wrongAnswers"] += 1
        data["Results"]["wrong"] += 1
    return data

def setNextDiff(data,request):
    numOfQuestions = data["Results"]["right"] + data["Results"]["wrong"]
    processing = {}
    for item, value in data["Themes"].items():
        processing[item] = (value["rightAnswers"]/data["Results"]["right"])*(data["Results"]["right"]/numOfQuestions)
    minVal = processing[min(processing, key=processing.get)]
    maxVal = processing[max(processing, key=processing.get)]
    for item, value in processing.items():
        p = (processing[item]-minVal)/(maxVal-minVal)
        data["Themes"][item]["normalizedValue"] = p
        data["Themes"][item]["currDiff"] = getNextDiff(p,data["Themes"][item]["currDiff"])
    with open(request.session['filePath']) as f:
        dt = json.load(f)
    dt.update(data)
    with open(request.session['filePath'], 'w') as f:
        json.dump(dt, f)
    l = irtParams(request)
    return l

def irtParams(req):
    res,resq = [],[]
    p,q,al,b=0,0,0,0
    with open(req.session['filePath']) as f:
        data = json.load(f)
    print(data['Results']['right'],data['Results']['wrong'])
    al = data['Results']['right']+data['Results']['wrong']
    p = data['Results']['right']/(al)
    q = 1-p
    th = math.log(p/q)
    print('-------------УРОВЕНЬ ЗНАНИЙ')
    print(th)
    res.append({'X':data['Results']['right'],'p':p,'q':q,'q0':th,'q2':th**2})
    for item in req.session['exclude']:
        for k,v in item.items():
            resq.append({'b0':v,'b2':v**2})

    ath=1.2718427033479196
    ab=1.1331282692461255
    ths=0.4500327522525397
    bs=-0.30451559227267
    sth=0.5073209808147314
    sb=1.3900144750457495

    srq = [x['q0']*ath+bs for x in res]
    #print(res)
    #print(srq)
    print(ath/math.sqrt(al*res[0]['p']*res[0]['q']))
    return srq[0]
