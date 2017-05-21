from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views
app_name='tests'
urlpatterns = [
    url(r'^$', login_required(views.IndexView.as_view()), name='indexSub'),
    url(r'^setInitialParams/(?P<subjectID>[0-9]+)/$', views.setInitialParams, name='setInitialParams'),
    url(r'^startTesting/$', views.startTesting, name='startTesting'),
    url(r'^studentAnswer/(?P<themeID>[0-9]+)/(?P<questionID>[0-9]+)/$', views.studentAnswer, name='studentAnswer'),
    url(r'^getNextQuestion/$', views.getNextQuestion, name='getNextQuestion'),
    url(r'^usersTests/$', views.usersTests, name='usersTests'),
    url(r'^usersTests/(?P<resultsID>[0-9]+)/$', views.resultDetails, name='resultDetails'),
    url(r'^usersTests/detailedReport/(?P<resultsID>[0-9]+)/$', views.detailedReport, name='detailedReport'),
    url(r'^uploadFile/$', views.uploadFile, name='uploadFile'),
    url(r'^myTests/$', views.myTests, name='myTests'),
    url(r'^testDetails/(?P<testID>[0-9]+)/$', views.testDetails, name='testDetails'),
    url(r'^groupsTestDetails/(?P<testID>[0-9]+)/$', views.groupsTestDetails,name='groupsTestDetails'),
    url(r'^usersTestDetails/(?P<testID>[0-9]+)/$', views.usersTestDetails,name='usersTestDetails'),
    url(r'^delete/$', views.deleteTest, name='deleteTest'),
    url(r'^questionCreate/$', views.questionCreate, name='questionCreate'),
    url(r'^questionEdit/$', views.questionEdit, name='questionEdit'),
    url(r'^questionDelete/$', views.questionDelete, name='questionDelete'),
]
