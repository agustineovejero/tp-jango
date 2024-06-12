import csv
import datetime
from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
import matplotlib.pyplot as plt

from polls.models import Equipos, Fichaje, Persona, Temporada, Valor, Club

def load_dataset(request):
    with open("datasetT.csv") as file:
        reader= csv.reader(file, delimiter=";")
        next(reader)

        persons = []
        signings = []
        teams = []
        values = []
        seasons = []
        clubs = []

        Persona.objects.all().delete()
        Fichaje.objects.all().delete()
        Equipos.objects.all().delete()
        Temporada.objects.all().delete()
        Valor.objects.all().delete()
        Club.objects.all().delete()


        for row in reader:
            print(row)
            name, position, age, height, foot, signing, previous_team, market_value, season, club = row

            
            if age == "-":
                age = 0
            age = age.replace("†", "")
            
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

            height = float(height)

            persons.append(
                Persona(
                    name=name,
                    position=position,
                    age=age,
                    height=height,
                    foot=foot,
                ))
            signings.append(
                Fichaje(
                    signing=signing,
                ))

            teams.append(
                Equipos(
                    previous_team=previous_team,
                ))
            values.append(
                Valor(
                    market_value=market_value,
                ))
            seasons.append(
                Temporada(
                    season=season,
                ))
            clubs.append(
                Club(
                    club=club,
                ))
        
        Persona.objects.bulk_create(persons)
        Fichaje.objects.bulk_create(signings)
        Equipos.objects.bulk_create(teams)
        Valor.objects.bulk_create(values)
        Temporada.objects.bulk_create(seasons)
        Club.objects.bulk_create(clubs)

        return HttpResponse("ok")




