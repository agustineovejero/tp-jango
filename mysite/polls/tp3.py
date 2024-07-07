import io
import csv
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db import models
from polls.models import Player, Club, Signing

def index(request):
    context = {
        'timestamp': timezone.now().timestamp()  # Add a timestamp to bust cache
    }
    return render(request, 'tp3.html', context)

def clubs(request):
    clubs = Club.objects.all()
    return render(request, 'clubs.html', {'clubs': clubs})

def create_figure():
    """Helper function to create a new figure."""
    fig, ax = plt.subplots()
    return fig, ax

def save_figure_to_buffer(fig):
    """Helper function to save figure to a BytesIO buffer."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return buf

def club_details(request, club_id):
    # Retrieve the club based on the club_id
    club = get_object_or_404(Club, id=club_id)
    
    # Retrieve all signings for this club
    signings = Signing.objects.filter(club=club).select_related('player')
    
    # Calculate total players and average market value
    total_players = signings.count()
    average_market_value = signings.aggregate(models.Avg('market_value'))['market_value__avg'] or 0
    
    context = {
        'club': club,
        'total_players': total_players,
        'average_market_value': average_market_value,
        'signings': signings
    }
    
    return render(request, 'club.html', context)


def import_csv(request):
    # Clear the tables
    Player.objects.all().delete()
    Club.objects.all().delete()
    Signing.objects.all().delete()
    
    with open('DatasetT.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            # Check if the club already exists in the database
            club, _ = Club.objects.get_or_create(name=row['Club'])

            # Parse age
            age = int(row['Edad'].replace('†', '')) if row['Edad'] else None

            # Parse height
            height = float(row['Altura'].replace(',', '.')) if row['Altura'] else None

            # Check if the player already exists in the database
            player, _ = Player.objects.get_or_create(
                name=row['Jugadores'],
                defaults={
                    'position': row['Posicion'],
                    'age': age,
                    'height': height,
                    'preferred_foot': row['Pie']
                }
            )

            # Parse the date, handle missing or incorrect formats
            date_signed = datetime.strptime(row['Fichado'], '%d/%m/%Y') if row['Fichado'] else None

            # Parse market value
            market_value = int(row['Valor de mercado']) if row['Valor de mercado'] else None

            # Create a signing object
            Signing.objects.create(
                player=player,
                club=club,
                date_signed=date_signed,
                previous_team=row['Equipo Anterior'] if row['Equipo Anterior'] != '-' else None,
                market_value=market_value,
                season=int(row['Temporada'])
            )

    return HttpResponse("CSV data imported successfully.")

def ages_by_season(request):
    last_three_seasons = Signing.objects.order_by('-season').values_list('season', flat=True).distinct()[:3]
    signings = Signing.objects.filter(season__in=last_three_seasons)
    
    data = {}
    for signing in signings:
        season = signing.season
        age = signing.player.age
        if season not in data:
            data[season] = {}
        if age not in data[season]:
            data[season][age] = 0
        data[season][age] += 1
    
    fig, ax = create_figure()
    
    seasons = sorted(data.keys())
    ages = sorted({age for season_data in data.values() for age in season_data.keys()})
    
    bar_width = 0.8 / len(ages)
    
    for i, age in enumerate(ages):
        counts = [data[season].get(age, 0) for season in seasons]
        bar_positions = [j + i * bar_width for j in range(len(seasons))]
        ax.bar(bar_positions, counts, bar_width, label=f'Age {age}')
    
    ax.set_xlabel('Season')
    ax.set_ylabel('Number of Players')
    ax.set_title('Sum of Players Grouped by Age per Season')
    ax.set_xticks([j + bar_width * (len(ages) / 2 - 0.5) for j in range(len(seasons))])
    ax.set_xticklabels(seasons)
    ax.legend()
    
    buf = save_figure_to_buffer(fig)
    plt.close(fig)
    
    return HttpResponse(buf, content_type='image/png')

def top_10_clubs_expensive_players(request):
    top_clubs = Club.objects.annotate(total_market_value=models.Sum('signing__market_value')).order_by('-total_market_value')[:10]
    
    club_names = [club.name for club in top_clubs]
    market_values = [club.total_market_value for club in top_clubs]
    
    fig, ax = create_figure()
    ax.bar(club_names, market_values)
    ax.set_xlabel('Club')
    ax.set_ylabel('Total Market Value')
    ax.set_title('Top 10 Clubs with the Most Expensive Players')
    ax.tick_params(axis='x', rotation=45)
    
    buf = save_figure_to_buffer(fig)
    plt.close(fig)
    
    return HttpResponse(buf, content_type='image/png')

def top_10_expensive_players(request):
    top_players = Player.objects.annotate(total_market_value=models.Max('signing__market_value')).order_by('-total_market_value')[:10]
    
    player_names = [player.name for player in top_players]
    market_values = [player.total_market_value for player in top_players]
    
    fig, ax = create_figure()
    ax.bar(player_names, market_values)
    ax.set_xlabel('Player')
    ax.set_ylabel('Market Value')
    ax.set_title('Top 10 Most Expensive Players')
    ax.tick_params(axis='x', rotation=45)
    
    buf = save_figure_to_buffer(fig)
    plt.close(fig)
    
    return HttpResponse(buf, content_type='image/png')

def top_10_expensive_players_json(request):
    top_players = Player.objects.annotate(total_market_value=models.Max('signing__market_value')).order_by('-total_market_value')[:10]
    
    players_data = [
        {
            'name': player.name,
            'total_market_value': player.total_market_value
        }
        for player in top_players
    ]
    
    return JsonResponse(players_data, safe=False)

def preferred_foot_distribution(request):
    right_footed_count = Player.objects.filter(preferred_foot='derecho').count()
    left_footed_count = Player.objects.filter(preferred_foot='izquierdo').count()
    
    labels = ['Right Footed', 'Left Footed']
    sizes = [right_footed_count, left_footed_count]
    colors = ['#ff9999','#66b3ff']
    
    fig, ax = create_figure()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')
    ax.set_title('Distribution of Players by Preferred Foot')
    
    buf = save_figure_to_buffer(fig)
    plt.close(fig)
    
    return HttpResponse(buf, content_type='image/png')
