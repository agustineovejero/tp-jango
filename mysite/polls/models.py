from django.db import models
class Persona(models.Model):
    name = models.CharField(max_length=100)
    position= models.CharField(max_length=100)
    age= models.IntegerField()
    height= models.IntegerField()
    foot=models.CharField(max_length=20)

class Fichaje(models.Model):
    Signing= models.DateField()

class Equipos(models.Model):
    PreviousTeam=models.CharField(max_length=100)

class Valor(models.Model):
    MarketValue=models.IntegerField()
    
class Temporada(models.Model):
    Season=models.IntegerField()

class Club(models.Model):
    Club=models.CharField(max_length=50)


    