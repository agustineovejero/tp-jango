import csv
import datetime
from django.shortcuts import render

from polls.models import Equipos, Fichaje, Persona, Temporada, Valor, Club

def load_dataset(request):
    with open("datasetT.csv") as file:
        reader= csv.reader(file, delimiter=";")
        next(reader)
        for row in reader:
            print(row)
            name, position, age, height, foot, signing, previous_team, market_value, season, club = row

            
            if age == "-":
                age = 0
            
            if market_value == "-":
                market_value = 0
            
            height = height.replace(',', '.')
            if height == "-":
                height = 0

            # Convert to YYYY-MM-DD format
            if signing == "-":
                signing = None
            else:
                date_obj = datetime.datetime.strptime(signing, "%d/%m/%Y")
                signing = date_obj.strftime("%Y-%m-%d")

            if market_value == "-":
                market_value = 0

            height = float()

            Persona.objects.create(name=name, age=age, position=position, height=height, foot=foot)
            Fichaje.objects.create(signing=signing)
            Equipos.objects.create(previous_team=previous_team)
            Valor.objects.create(market_value=market_value)
            Temporada.objects.create(season=season)
            Club.objects.create(club=club)
