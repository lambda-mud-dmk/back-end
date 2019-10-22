from django.contrib.auth.models import User
from adventure.models import Player, Room
import random

Room.objects.all().delete()
opposite_directions = {"n": "s", "s": "n", "e": "w", "w": "e"}
number_rooms = 100

r_outside = Room(title="Outside Cave Entrance",
                 description="North of you, the cave mount beckons")

r_foyer = Room(
    title="Foyer", description="""Dim light filters in from the south.""")

r_outside.save()
r_foyer.save()

# Link rooms together
r_outside.connectRooms(r_foyer, "n")
r_foyer.connectRooms(r_outside, "s")
previous_room = r_foyer
# Generate the rest of the rooms randomly
for n in range(number_rooms - 2):
    direction = None
    new_room = Room(title="DEFAULT TITLE",
                    description="DEFAULT DESCRIPTION")
    while direction is None:
        direction = random.choice(list(opposite_directions.keys()))
        if direction == "n" and previous_room.n_to is not 0:
            direction = None
        elif direction == "s" and previous_room.s_to is not 0:
            direction = None
        elif direction == "e" and previous_room.e_to is not 0:
            direction = None
        elif direction == "w" and previous_room.w_to is not 0:
            direction = None
        if direction is not None:
            new_room.save()
            previous_room.connectRooms(new_room, direction)
            new_room.connectRooms(
                previous_room, opposite_directions[direction])

            previous_room.save()
            new_room.save()
            previous_room = new_room


players = Player.objects.all()
for p in players:
    p.currentRoom = r_outside.id
    p.save()

rooms = Room.objects.all()
print(f"Generated {len(rooms)} rooms")
