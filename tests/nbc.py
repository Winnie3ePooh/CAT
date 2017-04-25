import numpy as np
import json

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

def setNextDiff(data):
    numOfQuestions = data["Results"]["right"] + data["Results"]["wrong"]
    processing = {}
    for item, value in data["Themes"].items():
        processing[item] = (value["rightAnswers"]/data["Results"]["right"])*(data["Results"]["right"]/numOfQuestions)
    print(processing)
    minVal = processing[min(processing, key=processing.get)]
    maxVal = processing[max(processing, key=processing.get)]
    print('---------------- {} ----- {}'.format(minVal,maxVal))
    for item, value in processing.items():
        p = (processing[item]-minVal)/(maxVal-minVal)
        data["Themes"][item]["normalizedValue"] = p
        data["Themes"][item]["currDiff"] = getNextDiff(p,data["Themes"][item]["currDiff"])
    print(data)
    return data
