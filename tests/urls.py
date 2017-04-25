from django.conf.urls import url

from . import views

app_name='tests'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='indexSub'),
    url(r'^(?P<subjectID>[0-9]+)/$', views.detailView, name='detailView'),
    url(r'^startTesting/(?P<subjectID>[0-9]+)/$', views.startTesting, name='startTesting'),
    url(r'^studentAnswer/(?P<themeID>[0-9]+)/(?P<questionID>[0-9]+)/(?P<cmplty>[0-9]+)/?', views.studentAnswer, name='studentAnswer'),
    url(r'^getNextQuestion/$', views.getNextQuestion, name='getNextQuestion'),
    url(r'^usersTests/$', views.usersTests, name='usersTests'),
    url(r'^usersTests/(?P<resultsID>[0-9]+)/$', views.testDetails, name='testDetails'),
    url(r'^usersTests/detailedReport/(?P<resultsID>[0-9]+)/$', views.detailedReport, name='detailedReport'),
    url(r'^uploadFile/$', views.uploadFile, name='uploadFile'),
]
