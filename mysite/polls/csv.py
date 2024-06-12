import csv
from datetime import datetime
from polls.models import Player, Club, Signing

def import_csv(request):
    with open('DatasetT.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            # Check if the club already exists in the database
            club, created = Club.objects.get_or_create(name=row['Club'])

            # Market value
            age = None
            if row['Edad']:
                try:
                    age = int(row['Edad'].replace('†', ''))
                except ValueError:
                    age = None

            # Market value
            height = None
            if row['Altura']:
                try:
                    height = float(row['Altura'].replace(',', '.'))
                except ValueError:
                    height = None

            # Check if the player already exists in the database
            player, created = Player.objects.get_or_create(
                name=row['Jugadores'],
                defaults={
                    'position': row['Posicion'],
                    'age': age,
                    'height': height,
                    'preferred_foot': row['Pie']
                }
            )

            # Parse the date, handle missing or incorrect formats
            date_signed = None
            if row['Fichado']:
                try:
                    date_signed = datetime.strptime(row['Fichado'], '%d/%m/%Y')
                except ValueError:
                    date_signed = None

            # Market value      
            market_value = None
            if row['Valor de mercado']:
                try:
                    market_value = int(row['Valor de mercado'])
                except ValueError:
                    market_value = None

            # Create a signing object
            signing = Signing.objects.create(
                player=player,
                club=club,
                date_signed=date_signed,
                previous_team=row['Equipo Anterior'] if row['Equipo Anterior'] != '-' else None,
                market_value=market_value,
                season=int(row['Temporada'])
            )
