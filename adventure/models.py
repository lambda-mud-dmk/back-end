from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid


class Room(models.Model):
    row = models.IntegerField(default=0)
    column = models.IntegerField(default=0)
    title = models.CharField(max_length=50, default="DEFAULT TITLE", null=True)
    description = models.CharField(
        max_length=500, default="DEFAULT DESCRIPTION", null=True)
    wall_n = models.BooleanField(default=True)
    wall_s = models.BooleanField(default=True)
    wall_e = models.BooleanField(default=True)
    wall_w = models.BooleanField(default=True)

    def knock_down_wall(self, other, wall):
        # A wall separates a pair of cells in the N-S or W-E directions.
        wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
        if wall == 'N':
            self.wall_n = False
            other.wall_s = False
        elif wall == 'S':
            self.wall_s = False
            other.wall_n = False
        elif wall == 'E':
            self.wall_e = False
            other.wall_w = False
        elif wall == 'W':
            self.wall_w = False
            other.wall_e = False
        self.save()
        other.save()

    def has_all_walls(self):
        if self.wall_n and self.wall_s and self.wall_e and self.wall_w:
            return True
        else:
            return False

    def playerNames(self, currentPlayerID):
        return [p.user.username for p in Player.objects.all()]

    def playerUUIDs(self, currentPlayerID):
        return [p.uuid for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentRoom = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def initialize(self):
        if self.currentRoom == 0:
            self.currentRoom = Room.objects.first().id
            self.save()

    def room(self):
        try:
            return Room.objects.get(id=self.currentRoom)
        except Room.DoesNotExist:
            self.initialize()
            return self.room()


@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()
