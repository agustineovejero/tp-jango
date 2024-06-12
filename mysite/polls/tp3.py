import io

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.shortcuts import render
from polls.models import Signing

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


def top_10_expensive_signings(request):
    # Query the top 10 most expensive signings
    top_signings = Signing.objects.order_by('-market_value')[:10]
    
    # Prepare data
    players = [signing.player.name for signing in top_signings]
    values = [signing.market_value for signing in top_signings]
    
    # Create plot
    fig, ax = plt.subplots()
    ax.bar(players, values)
    ax.set_xlabel('Player')
    ax.set_ylabel('Market Value')
    ax.set_title('Top 10 Most Expensive Signings')
    ax.tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better readability
    
    # Save plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    
    return HttpResponse(buf, content_type='image/png')