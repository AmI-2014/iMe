from django.db import models


class Checkpoint(models.Model):
    name = models.CharField(max_length=50)
    coordinates = models.CharField(max_length=20)
    prox = models.IntegerField()
    def __unicode__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=20)
    rank = models.IntegerField(default=0)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ('name',)


class Lobby(models.Model):
    lobby_name = models.CharField(max_length=40)
    max_range = models.IntegerField(default=0)
    players = models.ManyToManyField(Player, related_name="giocatore")
    def __unicode__(self):
        return self.lobby_name
    class Meta:
        ordering = ('lobby_name',)


