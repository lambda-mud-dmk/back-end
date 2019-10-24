from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from adventure.models import Room, Player
from django.http import JsonResponse
import json
import random


class Maze:
    def __init__(self, number_rows, number_columns, ix=0, iy=0):
        self.number_rows, self.number_columns = number_rows, number_columns
        self.ix, self.iy = ix, iy
        Room.objects.all().delete()
        self.maze_map = [[Room(row=x, column=y)
                          for y in range(number_columns)] for x in range(number_rows)]
        for x in range(self.number_rows):
            for y in range(self.number_columns):
                self.maze_map[x][y].save()

    def room_at(self, x, y):
        return self.maze_map[x][y]

    def find_valid_neighbours(self, room):
        delta = [('W', (0, -1)),
                 ('E', (0, 1)),
                 ('S', (1, 0)),
                 ('N', (-1, 0))]
        neighbours = []
        for direction, (dx, dy) in delta:
            x2, y2 = room.row + dx, room.column + dy
            if (0 <= x2 < self.number_rows) and (0 <= y2 < self.number_columns):
                neighbour = self.room_at(x2, y2)
                if neighbour.has_all_walls():
                    neighbours.append((direction, neighbour))
        return neighbours

    def create_maze(self):
        n = self.number_rows * self.number_columns
        room_stack = []
        current_room = self.room_at(self.ix, self.iy)
        visited_rooms = 1

        while visited_rooms < n:
            neighbours = self.find_valid_neighbours(current_room)
            if not neighbours:
                current_room = room_stack.pop()
                continue

            direction, next_room = random.choice(neighbours)
            current_room.knock_down_wall(next_room, direction)
            room_stack.append(current_room)
            current_room = next_room
            visited_rooms += 1

    def toList(self):
        maze = []
        rooms = Room.objects.all()
        for room in rooms:
            maze.append({
                'row': room.row,
                'column': room.column,
                'wall_n': room.wall_n,
                'wall_s': room.wall_s,
                'wall_e': room.wall_e,
                'wall_w': room.wall_w
            })
        return maze


rows = 10
columns = 10
maze = Maze(rows, columns)
maze.create_maze()
players = Player.objects.all()
for p in players:
    p.currentRoom = Room.objects.all().first().id
    p.save()

print({
    'rows': rows,
    'columns': columns,
    'maze': maze.toList()
})
