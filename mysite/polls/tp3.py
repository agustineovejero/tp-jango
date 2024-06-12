import io

import matplotlib

from polls.models import models


matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.shortcuts import render
from polls.models import Club, Player, Signing

def index(request):
    return render(request, 'tp3.html')

def ages_by_season(request):
    # Query data for the last three seasons
    last_three_seasons = Signing.objects.order_by('-season').values_list('season', flat=True).distinct()[:3]
    signings = Signing.objects.filter(season__in=last_three_seasons)
    
    # Prepare data
    data = {}
    for signing in signings:
        season = signing.season
        age = signing.player.age
        if season not in data:
            data[season] = {}
        if age not in data[season]:
            data[season][age] = 0
        data[season][age] += 1
    
    # Create plot
    fig, ax = plt.subplots()
    
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
    
    # Save plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    
    return HttpResponse(buf, content_type='image/png')



def top_10_clubs_expensive_players(request):
    # Query the top 10 clubs with the most expensive players
    top_clubs = Club.objects.annotate(total_market_value=models.Sum('signing__market_value')).order_by('-total_market_value')[:10]
    
    # Prepare data
    club_names = [club.name for club in top_clubs]
    market_values = [club.total_market_value for club in top_clubs]
    
    # Create plot
    fig, ax = plt.subplots()
    ax.bar(club_names, market_values)
    ax.set_xlabel('Club')
    ax.set_ylabel('Total Market Value')
    ax.set_title('Top 10 Clubs with the Most Expensive Players')
    ax.tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better readability
    
    # Save plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    
    return HttpResponse(buf, content_type='image/png')






def top_10_expensive_players(request):
    # Query the top 10 most expensive players
    top_players = Player.objects.annotate(total_market_value=models.Max('signing__market_value')).order_by('-total_market_value')[:10]
    
    # Prepare data
    player_names = [player.name for player in top_players]
    market_values = [player.total_market_value for player in top_players]
    
    # Create plot
    fig, ax = plt.subplots()
    ax.bar(player_names, market_values)
    ax.set_xlabel('Player')
    ax.set_ylabel('Market Value')
    ax.set_title('Top 10 Most Expensive Players')
    ax.tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better readability
    
    # Save plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    
    return HttpResponse(buf, content_type='image/png')



def preferred_foot_distribution(request):
    # Query data
    right_footed_count = Player.objects.filter(preferred_foot='derecho').count()
    left_footed_count = Player.objects.filter(preferred_foot='izquierdo').count()
    
    # Prepare data
    labels = ['Right Footed', 'Left Footed']
    sizes = [right_footed_count, left_footed_count]
    colors = ['#ff9999','#66b3ff']
    
    # Create pie chart
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_title('Distribution of Players by Preferred Foot')
    
    # Save plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    
    return HttpResponse(buf, content_type='image/png')