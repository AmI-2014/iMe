from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from math import radians, fabs, sin, cos, acos, floor
import datetime
import json
from hello.models import Player, Checkpoint, Lobby
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt


 # Given a string of coordinates, returns a list with latitude and longitude in radians
def coordstr2rad(string):
    temp=string.split(",")
    coordinates=[]
    coordinates.append(radians(float(temp[0])))
    coordinates.append(radians(float(temp[1])))
    return coordinates
# Given two strings of coordinates in radians, returns the distance between them in meters
def distance_between_coordinates(str1,str2): 
    coord1=coordstr2rad(str1)
    coord2=coordstr2rad(str2)
    fi=fabs(coord1[1]-coord2[1])
    P = acos((sin(coord1[0]) * sin(coord2[0]))+(cos(coord1[0]) * cos(coord2[0]) * cos(fi)))
    return P*6372795.477598

#accepts POST requests using the name of the new player for the initialization, taken as POST parameter. Returns the player's ID
@csrf_exempt
def player_initialization(request):
    if request.method == 'POST':
        new_name = request.POST.get('name')
        new_player = Player(name = new_name, rank = 0)
        new_player.save()
        return HttpResponse(new_player.id)

#accepts POST requests using the new name for the player for updating it, taken as POST parameter. Returns 'ok'
@csrf_exempt
def player_update(request):
    if request.method == 'POST':
        new_name = request.POST.get('name')
        pk = request.POST.get('id')
        old_player = Player.objects.get(id=pk)
        old_player.name = new_name
        old_player.save()
        return HttpResponse('OK')

#Accepts POST requests using the name of the lobby to create a new one and the player's ID to make him join the lobby itself. Both the lobby's name and the player's ID are taken as POST parameters. Obviously the player must already exist. Returns 'ok'. Check for existing lobby still missing. [exists()]
@csrf_exempt
def create_lobby(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        player_id = request.POST.get('id') 
        new_lobby = Lobby(lobby_name = name, max_range = 0, game_nrc='NULL')
        new_lobby.save()
        associated_player = Player.objects.get(id=player_id)
        if associated_player!=None:
            new_lobby.players.add(associated_player) 
            new_lobby.save()
            return HttpResponse('OK')


#Unique name of lobby is given
@csrf_exempt   
def join_lobby(request):
    #join an existing lobby. Accepts GET request to the server, which response is the existing lobbies
    if request.method == 'GET':
		#if no json serialization will be required uncomment the following line and fix the return
		#total_lobbies = Lobby.objects.all()
        parsed_total_lobby = serializers.serialize("json", Lobby.objects.all())
        return HttpResponse(parsed_total_lobby, mimetype='application/json')

    #actual join-existing-lobby function. Accepts POST requests with lobby's name and player ID as params
    elif request.method == 'POST':
        l_name = request.POST.get('name')
        player_id = request.POST.get('id')
        lobby = Lobby.objects.get(lobby_name=l_name)
        player = Player.objects.get(id=player_id)
        lobby.players.add(player)
        lobby.save()
        return HttpResponse('OK')

@csrf_exempt
def distance(request):
    c1 = request.POST.get('point1')
    c2 = request.POST.get('point2')
    d=distance_between_coordinates(c1,c2)
    return HttpResponse(d)

@csrf_exempt
def search_for_checkpoints(request):
    if request.method == 'POST':
        lobby_n = request.POST.get('lobby')
        num_check = int(request.POST.get('first'))
        play_range = float(request.POST.get('second'))
        start_coord = request.POST.get('third')
        lobby = Lobby.objects.get(lobby_name=lobby_n)
        string = str(num_check)+"-"+str(play_range)+"-"+start_coord
        lobby.game_nrc = string
        possible_checkpoints = 0

        for e in Checkpoint.objects.all():
            c = e.coordinates
            meters = distance_between_coordinates(c,start_coord)
            if meters <= play_range:
                possible_checkpoints = possible_checkpoints+1
        
        max_players = int(floor(possible_checkpoints/(num_check*1.5)))
            
        return HttpResponse(max_players) 
            
            
            
        
        






