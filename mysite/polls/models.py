from django.db import models
class Persona(models.Model):
    jugadores = models.CharField(max_length=100)
    posiciones= models.CharField(max_length=100)
    edad= models.IntegerField()
    altura= models.IntegerField()
    pie=models.CharField(max_length=20)

class fichaje(models.Model):
    fichaje= models.DateField()

class Equipos(models.Model):
    Equipoanterior=models.CharField(max_length=100)

class Valor(models.Model):
    ValordeMercado=models.IntegerField()
    
class Temporada(models.Model):
    temporada=models.IntegerField()

class Club(models.Model):
    Club=models.CharField(max_length=50)


    