from django.urls import path
from polls import tp3

urlpatterns = [
    path("csv", tp3.import_csv, name="csv"),
    path("", tp3.index, name="index"),
    path('clubs', tp3.clubs, name='clubs'),
    path('clubs/<int:club_id>/', tp3.club_details, name='club_details'),
    path('agesbyseason.png', tp3.ages_by_season, name='ages_by_season'),
    path('expensiveclubs.png', tp3.top_10_clubs_expensive_players, name='top_10_clubs_expensive_players'),
    path('expensiveplayers.png', tp3.top_10_expensive_players, name='top_10_expensive_players'),
    path('expensiveplayers.json', tp3.top_10_expensive_players_json, name='top_10_expensive_players_json'),
    path('preferredfoot.png', tp3.preferred_foot_distribution, name='preferred_foot_distribution'),
]
