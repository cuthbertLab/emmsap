from django.conf.urls import url

from . import views

app_name = 'emmsap'
urlpatterns = [
    # ex: /emmsap/
    url(r'^$', views.index, name='index'),
    # ex: /emmsap/composer/5/
    url(r'^composer/(?P<composerId>[0-9]+)/', views.composer, name='composer'),
    # ex: /emmsap/composer/list/
    url(r'^composer/list/', views.listComposers, name='listComposers'),

    # ex: /emmsap/piece/193/assignComposer/  
    url(r'^piece/(?P<pieceId>[0-9]+)/assignComposer/', views.assignComposer, name='assignComposer'),
    url(r'^piece/(?P<pieceId>[0-9]+)/assignComposerFollowup/', views.assignComposerFollowup, name='assignComposerFollowup'),
    # ex: /emmsap/composer/5/
    # url(r'^piece/(?P<pieceId>[0-9]+)/', views.piece, name='piece'),



    url(r'^upload/', views.uploadFile, name='upload'),
]