from django.http import HttpResponse, HttpRequest
from django.shortcuts import render   
from math import radians, fabs, sin, cos, acos, floor
import operator
import datetime
from django.utils.timezone import utc
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

'''
accepts POST requests using the name of the new player for the initialization, taken as POST parameter. 
Returns 'NOK' if name already exists, the player's id otherwise.
'''
@csrf_exempt
def player_initialization(request):

    if request.method == 'POST':
        new_name = request.POST.get('name')

        if Player.objects.filter(name = new_name).exists() == True:
            return HttpResponse("NOK")

        else:
            new_player = Player(name = new_name, checked = 0)
            new_player.save()

            return HttpResponse(new_player.id)

'''
accepts POST requests using the new name for the player for updating it, taken as POST parameter. Returns 'ok'
'''
@csrf_exempt
def player_update(request):

    if request.method == 'POST':
        new_name = request.POST.get('name')
        pk = request.POST.get('id')
        old_player = Player.objects.get(id=pk)
        old_player.name = new_name
        old_player.save()

        return HttpResponse('OK')

'''
 Accepts POST requests using the name of the lobby to create a new one and the player's ID to make him
 join the lobby itself. Both the lobby's name and the player's ID are taken as POST parameters. Obviously
 the player must already exist. Returns 'NOK' if lobby's name already exists, 'OK' otherwise.
''' 
@csrf_exempt
def create_lobby(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        player_id = request.POST.get('id') 
        if Lobby.objects.filter(lobby_name = name).exists() == True:
            return HttpResponse("NOK")
        
        else: 
            if Lobby.objects.filter(players__pk = player_id).exists() == True:
                old_lobby = Lobby.objects.get(players__pk = player_id)
                player = Player.objects.get(id = player_id)
                old_lobby.players.remove(player)
                old_lobby.save()
                now = datetime.datetime.utcnow().replace(tzinfo=utc)
                new_lobby = Lobby(lobby_name = name, game_nrcd ='NULL', game_status = False, game_start_date = now)
                new_lobby.save()
                associated_player = player
                new_lobby.players.add(player) 
                new_lobby.save()     
            else:
                player = Player.objects.get(id = player_id)
                now = datetime.datetime.utcnow().replace(tzinfo=utc)
                new_lobby = Lobby(lobby_name = name, game_nrcd ='NULL', game_status = False, game_start_date = now)
                new_lobby.save()
                associated_player = player
                new_lobby.players.add(player) 
                new_lobby.save()                


            return HttpResponse('OK')


@csrf_exempt   
def join_lobby(request):

    #join an existing lobby. Accepts GET request to the server, which response is the existing lobbies
    if request.method == 'GET':

        parsed_total_lobby = serializers.serialize("json", Lobby.objects.all())

        return HttpResponse(parsed_total_lobby, mimetype='application/json')

    #actual join-existing-lobby function. Accepts POST requests with lobby's name and player's ID as params
    elif request.method == 'POST':
        new_lobby = request.POST.get('name')
        player_id = request.POST.get('id')
        player = Player.objects.get(id = player_id)

        if Lobby.objects.filter(players__pk = player_id).exists() == True:
            old_lobby = Lobby.objects.get(players__pk = player_id)
            old_lobby.players.remove(player)
            old_lobby.save()
            lobby = Lobby.objects.get(lobby_name=new_lobby)
            lobby.players.add(player)
            lobby.save()
        
        else:
            lobby = Lobby.objects.get(lobby_name=new_lobby)
            lobby.players.add(player)
            lobby.save()            

        return HttpResponse('OK')


'''
 Accepts POST requests with the number of checkpoints, the range of play, the difficulty, the start
 coordinates and the lobby the creator belongs to as params. Returns the maximum number of players allowed
 for the created game.
'''
@csrf_exempt
def search_for_checkpoints(request):

    if request.method == 'POST':
        lobby_n = request.POST.get('lobby')
        num_check = int(request.POST.get('first'))
        play_range = float(request.POST.get('second'))
        start_coord = request.POST.get('third')
        difficulty = request.POST.get('fourth')
        lobby = Lobby.objects.get(lobby_name=lobby_n)
        string = str(num_check)+"-"+str(play_range)+"-"+start_coord+"-"+str(difficulty)
        lobby.game_nrcd = string
        lobby.save()
        possible_checkpoints = 0

        for e in Checkpoint.objects.all():
            c = e.coordinates
            meters = distance_between_coordinates(c,start_coord)
            if meters <= play_range:
                possible_checkpoints = possible_checkpoints+1
                lobby.checkpoints_under_range.add(e)        #associates valid checkpoints to the game/lobby 
                lobby.save()

        max_players = int(floor(possible_checkpoints/(num_check*2)))   

        return HttpResponse(max_players) 
            

'''
 Accepts POST requests with the player's id as param. Returns the json serialized checkpoints randomly
 choosen from the database, with a margin of the +100% on the number of requested checkpoints, within the
 selected range of play.
'''
@csrf_exempt
def get_checkpoints(request):

    if request.method == 'POST':
     
        player_id = request.POST.get('id')
        lobby = Lobby.objects.get(players__pk = player_id) 
        game_params = lobby.game_nrcd
        temp = game_params.split("-")
        checkpoints_needed = floor(int(temp[0])*2)
        #retrieve from database the proper number of checkpoints (randomly ordered) and send them in json
        checkpoints = lobby.checkpoints_under_range.order_by('?')[:checkpoints_needed]
        parsed_checkpoints = serializers.serialize("json", checkpoints)      
  
        return HttpResponse(parsed_checkpoints, mimetype='application/json')


'''
 Accepts POST requests with the player's id and the number of checkpoints checked as params. Returns a
 list of tuples containing all the players involved in the game sorted by the number of checkpoints
 completed; where the number is equal, the order is alphabetical.
'''
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

        dd = {} #following lines needed only to accomplish a proper response with a proper layout
        for i in tot_players:
            dd[i.name] = i.checked
        sorted_dd = sorted(dd.iteritems(), key=operator.itemgetter(1))

        return HttpResponse(simplejson.dumps(sorted_dd), content_type = 'application/json; charset = utf8')


'''
 Accepts POST request with the player's id. Returns the status of the game the player is associated with,
 as True if in progress, False if ended or not even started.
'''
@csrf_exempt
def game_status(request):

    if request.method == 'POST':
        player_id = request.POST.get('id')
        lobby = Lobby.objects.get(players__pk=player_id)
        return HttpResponse(lobby.game_status)

'''
 Accepts POST requests using player's ID as param. Returns the time delta since the beginning of the game
 in the following format h:m:s.us
'''
@csrf_exempt
def check_time(request):
    if request.method == 'POST':
        player_id = request.POST.get('id')
        lobby = Lobby.objects.get(players__pk=player_id)
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        delta = now - lobby.game_start_date
        return HttpResponse(delta)
        

'''
 Accepts POST request using as parameters the player's id and a boolean variable which is False if the
 player has completed his checkpoints. In this case every player finishing the game can use this function.
 On the other hand the same function called with True as parameter value should be a prerogative of the
 creator, which starts the game. The server returns an 'OK'
'''
@csrf_exempt
def begin_finish(request):

    if request.method =='POST':
        started = request.POST.get('yes_no')
        player_id = request.POST.get('id')
        lobby = Lobby.objects.get(players__pk=player_id)
        lobby.game_status = started
        if lobby.game_status == True:    
            now = datetime.datetime.utcnow().replace(tzinfo=utc)
            lobby.game_start_date = now   
            lobby.save()

        else:
            lobby.save()

        return HttpResponse('OK')

           


