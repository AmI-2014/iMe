from django.conf.urls import patterns, include, url


urlpatterns = [
    url(r'^PlayerInit/$', 'hello.views.player_initialization'),
    url(r'^PlayerUpdate/$', 'hello.views.player_update'),
    url(r'^CreateLobby/$', 'hello.views.create_lobby'),
    url(r'^JoinLobby/$', 'hello.views.join_lobby'),
    url(r'^SearchForCheckpoints/$','hello.views.search_for_checkpoints'),
    url(r'^GetCheckpoints/$', 'hello.views.get_checkpoints'),
    url(r'^Ranking/$', 'hello.views.ranking'),
    url(r'^GameStatus/$', 'hello.views.game_status'),
    url(r'^CheckTime/$', 'hello.views.check_time'),
    url(r'^BeginFinish/$', 'hello.views.begin_finish'),
]

