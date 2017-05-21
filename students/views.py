from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from registration.forms import RegistrationForm
from .forms import *
from django.contrib.auth import login

import datetime

def index(request):
    return render(request,'index.html')

def details(request):
    user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            return HttpResponseRedirect('/')
    else:
        form = UserForm(instance=user)
    return render(request,'students/userInfo.html',{'context': request.user,'form':form})

def allUsers(request):
    all_users = User.objects.all().order_by('username')
    paginator = Paginator(all_users, 10) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        users = paginator.page(paginator.num_pages)

    return render(request, 'students/index.html', {'users': users})

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        print(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            group = StudyGroup.objects.get(pk=request.POST['groupName'])
            print(group)
            profile = UserProfile(user=user,studygroup=group)
            profile.save()
            registered = True
        else:
            user_form.errors#, profile_form.errors
        if registered:
            login(request, user)
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/')
    else:
        user_form = UserForm()
        profile = ProfileForm()
        profile = render_to_string('basePicker.html',{'form':profile},request)

    return render(request,
            'registration/registration_form.html',
            {'user_form': user_form,'form':profile} )
