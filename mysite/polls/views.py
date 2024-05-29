import csv
from django.shortcuts import render

from polls.models import Equipos, Fichaje, Persona, Temporada, Valor, Club

def load_dataset(request):
    with open("datasetT.csv") as file:
        reader= csv.reader(file, delimiter=";")
        next(reader)
        for row in reader:
            print(row)
            name, position, age, height, foot, signing, previousTeam, marketValue, season, club= row

            height = float(height.replace(',', '.'))

            Persona.objects.create(name=name, age=age, position=position, height=height, foot=foot)
            Fichaje.objects.create(signing=signing)
            Equipos.objects.create(previousTeam=previousTeam)
            Valor.objects.create(marketValue=marketValue)
            Temporada.objects.create(season=season)
            Club.objects.create(club=club)
