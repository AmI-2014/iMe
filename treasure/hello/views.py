from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
import datetime
import json
from hello.models import Player, Checkpoint, Lobby
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def player_initialization(request):
    if request.method == 'POST':
        new_name = request.POST.get('name')
        new_player = Player(name = new_name, rank = 0)
        new_player.save()
        return HttpResponse(new_player.id)

@csrf_exempt
def player_update(request):
    if request.method == 'POST':
        new_name = request.POST.get('name')
        pk = request.POST.get('id')
        old_player = Player.objects.get(id=pk)
        old_player.name = new_name
        old_player.save()
        return HttpResponse('OK')

#NOT PROPERLY WORKING
@csrf_exempt
def create_lobby(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        player_id = request.POST.get('id') 
        new_lobby = Lobby(lobby_name = name, max_range = 0)
        #new_lobby.save()
        associated_player = Player.objects.get(id=player_id)
        #new_lobby.players.add(associated_player) 
		#new_lobby.save()
        return HttpResponse(new_lobby)
        


        
   


