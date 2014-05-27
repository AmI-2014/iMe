from django.conf.urls import patterns, include, url


urlpatterns = [
    url(r'^PlayerInit/$', 'hello.views.player_initialization'),
    url(r'^PlayerUpdate/$', 'hello.views.player_update'),
    url(r'^CreateLobby/$', 'hello.views.create_lobby')
]