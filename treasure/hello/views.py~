from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from math import radians, fabs, sin, cos, acos, floor
import operator
from hello.models import Player, Checkpoint, Lobby
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson


#Given a string of coordinates, returns a list with latitude and longitude in radians
def coordstr2rad(string):

    temp=string.split(",")
    coordinates=[]
    coordinates.append(radians(float(temp[0])))
    coordinates.append(radians(float(temp[1])))

    return coordinates
#Given two strings of coordinates in radians, returns the distance between them in meters
def distance_between_coordinates(str1,str2): 

    coord1=coordstr2rad(str1)
    coord2=coordstr2rad(str2)
    phi=fabs(coord1[1]-coord2[1])
    P = acos((sin(coord1[0]) * sin(coord2[0]))+(cos(coord1[0]) * cos(coord2[0]) * cos(phi)))

    return P*6372795.477598

#accepts POST requests using the name of the new player for the initialization, taken as POST parameter. Returns the player's ID
@csrf_exempt
def player_initialization(request):

    if request.method == 'POST':
        new_name = request.POST.get('name')
        new_player = Player(name = new_name, checked = 0)
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
        new_lobby = Lobby(lobby_name = name, max_range = 0, game_nrc ='NULL', game_status = False)
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

#Accepts POST requests with the number of checkpoints, the range of play, the start coordinates and the lobby the creator belongs to as params. Returns the maximum number of players allowed for the created game.
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
        lobby.save()
        possible_checkpoints = 0

        for e in Checkpoint.objects.all():
            c = e.coordinates
            meters = distance_between_coordinates(c,start_coord)
            if meters <= play_range:
                possible_checkpoints = possible_checkpoints+1
        
        max_players = int(floor(possible_checkpoints/(num_check*1.5)))
        lobby.game_status = False #if the lobby has already played a different game, eventually ended   

        return HttpResponse(max_players) 
            

#Accepts POST requests with the plyayer's id as param. Returns the json serialized checkpoints randomly choosen from the database, with a margin of the 50% on the number of requested checkpoints.
@csrf_exempt
def get_checkpoints(request):

    if request.method == 'POST':
        player_id = request.POST.get('id')
        lobby = Lobby.objects.get(players__pk = player_id)
        game_params = lobby.game_nrc 
        temp = game_params.split("-")
        checkpoints_needed = floor(int(temp[0])*1.5)
        checkpoints = Checkpoint.objects.order_by('?')[:checkpoints_needed] #if no json serialization it's needed
        parsed_checkpoints = serializers.serialize("json", Checkpoint.objects.order_by('?')[:checkpoints_needed])

        return HttpResponse(parsed_checkpoints, mimetype='application/json')


#Accepts POST requests with the player's id as param. Returns a list of tuples containing all the players involved in the game sorted by the number of checkpoints completed; where the number is equal, the order is alphabetical.
@csrf_exempt
def ranking(request):

    if request.method == 'POST':
        player_id = request.POST.get('id')
        cp_checked = request.POST.get('checked')
        player2update = Player.objects.get(id=player_id)
        player2update.checked = cp_checked
        player2update.save()
        lobby = Lobby.objects.get(players__pk=player_id)
        lobby_players = lobby.players.all()
        tot_players = []

        for e in lobby_players:
            player = Player.objects.get(id=e.id)
            tot_players.append(player)

        dd = {} #following lines needed only for accomplish a proper response with a proper layout
        for i in tot_players:
            dd[i.name] = i.checked
        sorted_dd = sorted(dd.iteritems(), key=operator.itemgetter(1))

        return HttpResponse(simplejson.dumps(sorted_dd), content_type = 'application/json; charset = utf8')


#Accepts POST request with the player's id. Returns the status of the game the player is associated with, as True if finished, False if still going
@csrf_exempt
def game_status(request):

    if request.method == 'POST':
        player_id = request.POST.get('id')
        lobby = Lobby.objects.get(players__pk=player_id)

        return HttpResponse(lobby.game_status)


#Accepts POST request using as parameters the player's id and a boolean variable which is True if the player has completed his checkpoints. The server return an 'ok'
@csrf_exempt
def end_game(request):

    if request.method =='POST':
        ended = request.POST.get('yes_no')
        player_id = request.POST.get('id')
        lobby = Lobby.objects.get(players__pk=player_id)#following lines not really necessary, but for clarity
        lobby.game_status = ended
        lobby.save()

        return HttpResponse('OK')
        

    
        
        
            
            
        
        






