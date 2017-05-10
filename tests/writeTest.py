import glob
import json

from tests.models import Question, Answer

def writeAnswers(req,question,sAnswers,rAnswers):
    with open(req.session['filePath']) as f:
        data = json.load(f)
    toWrite = {
        'question':question.questionName,
        'sAnswers':[],
        'rAnswers':[],
        'lvl': 0
    }
    for item in sAnswers:
        try:
            toWrite['sAnswers'].append(Answer.objects.get(pk=item).answerText)
        except ValueError:
            toWrite['sAnswers'].append('Нет ответа')
    for item in rAnswers:
        toWrite['rAnswers'].append(Answer.objects.get(pk=item).answerText)
    toWrite['lvl'] = req.session['lvl']
    data['Answers'].append(toWrite)

    with open(req.session['filePath'], 'w') as f:
        json.dump(data, f)
