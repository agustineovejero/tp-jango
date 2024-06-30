from django.db import models

class Club(models.Model):
    name = models.CharField(max_length=100)

class Player(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    height = models.FloatField(null=True)
    preferred_foot = models.CharField(max_length=20)

class Signing(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    date_signed = models.DateField(null=True)
    previous_team = models.CharField(max_length=100, null=True)
    market_value = models.IntegerField(null=True)
    season = models.IntegerField()
