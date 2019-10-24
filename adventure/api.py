from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json

# instantiate pusher
# pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))


@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    players = []
    return JsonResponse({'uuid': uuid, 'name': player.user.username, 'title': room.title, 'description': room.description, 'players': players, 'room_id': room.id}, safe=True)


# @csrf_exempt
@api_view(["POST"])
def move(request):
    dirs = {"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    direction = data['direction']
    current_room = Room.objects.get(pk=player.currentRoom)
    nextRoom_coordinates = (-1, -1)
    if direction == "n":
        # going up one row
        if not current_room.wall_n:
            nextRoom_coordinates = (current_room.row-1, current_room.column)
    elif direction == "s":
        # going down one row
        if not current_room.wall_s:
            nextRoom_coordinates = (current_room.row+1, current_room.column)
    elif direction == "e":
        # move forward one column
        if not current_room.wall_e:
            nextRoom_coordinates = (current_room.row, current_room.column+1)
    elif direction == "w":
        # move back one column
        if not current_room.wall_w:
            nextRoom_coordinates = (current_room.row, current_room.column-1)
    try:
        next_room = Room.objects.get(
            row=nextRoom_coordinates[0], column=nextRoom_coordinates[1])
        player.currentRoom = next_room.id
        player.save()
        players = []
        return JsonResponse(
            {
                'name': player.user.username,
                'row': next_room.row,
                'column': next_room.column,
                'players': players,
                'room_id': next_room.id,
                'error_msg': ""
            }, safe=True)
    except Room.DoesNotExist:
        players = []
        return JsonResponse(
            {
                'name': player.user.username,
                'row': current_room.row,
                'column': current_room.column,
                'players': players,
                'room_id': current_room.id,
                'error_msg': "You cannot move that way."
            }, safe=True)

@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    return JsonResponse({'error': "Not yet implemented"}, safe=True, status=500)

# @csrf_exempt
@api_view(["GET"])
def get_rooms(request):
    # IMPLEMENT
    all_rooms = list(Room.objects.all().order_by('id').values())


    return JsonResponse({"room": all_rooms}, safe=True, status=200)
