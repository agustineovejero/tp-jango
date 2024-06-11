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
    # Query data
    signings = Signing.objects.all()
    
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
