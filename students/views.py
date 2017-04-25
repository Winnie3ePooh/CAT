from django.shortcuts import render


def index(request):
    return render(request,'index.html')

def details(request):
    return render(request,'students/userInfo.html',{'context': request.user})