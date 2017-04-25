import glob
import json

from tests.models import Question, Answer

def writeAnswers(req,question,sAnswers,rAnswers):
    with open(req.session['filePath']) as f:
        data = json.load(f)
    toWrite = {
        'question':question.questionName,
        'sAnswers':[],
        'rAnswers':[]
    }
    for item in sAnswers:
        toWrite['sAnswers'].append(Answer.objects.get(pk=item).answerText)
    for item in rAnswers:
        toWrite['rAnswers'].append(Answer.objects.get(pk=item).answerText)

    data['Answers'].append(toWrite)

    with open(req.session['filePath'], 'w') as f:
        json.dump(data, f)
