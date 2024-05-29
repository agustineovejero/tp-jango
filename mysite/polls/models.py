from django.db import models
class Persona(models.Model):
    name = models.CharField(max_length=100)
    position= models.CharField(max_length=100)
    age= models.IntegerField()
    height= models.IntegerField()
    foot=models.CharField(max_length=20)

class Fichaje(models.Model):
    signing= models.DateField(null=True)

class Equipos(models.Model):
    previous_team=models.CharField(max_length=100)

class Valor(models.Model):
    market_value=models.IntegerField()
    
class Temporada(models.Model):
    season=models.IntegerField()

class Club(models.Model):
    club=models.CharField(max_length=50)


    