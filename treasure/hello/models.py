from django.db import models


class Checkpoint(models.Model):
    name = models.CharField(max_length=50)
    coordinates = models.CharField(max_length=20)
    prox = models.IntegerField()
    def __unicode__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=20)
    checked = models.IntegerField(default=0)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ('name',)


class Lobby(models.Model):
    lobby_name = models.CharField(max_length=40, primary_key = True)
    players = models.ManyToManyField(Player, related_name="related_lobby")
    game_nrcd = models.CharField(max_length=50) #nrcd stays for NumberOfCheckpoints-Range-startCoordinates-Difficulty
    game_status = models.BooleanField()
    game_start_date = models.DateTimeField()
    def __unicode__(self):
        return self.lobby_name
    class Meta:
        ordering = ('lobby_name',)


