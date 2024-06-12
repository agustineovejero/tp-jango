from django.urls import path
from polls import tp3, csv


urlpatterns=[
 # path("",views.index, name= "index"),
    path("csv", csv.import_csv, name="csv"),
    path("tp3", tp3.index, name= "tp3"),
    path('tp3/agesbyseason.png', tp3.ages_by_season, name='ages_by_season'),
    path('tp3/expensiveclubs.png', tp3.top_10_clubs_expensive_players, name='top_10_clubs_expensive_players'),
    path('tp3/expensiveplayers.png', tp3.top_10_expensive_players, name='top_10_expensive_players'),
    path('tp3/preferredfoot.png', tp3.preferred_foot_distribution, name='preferred_foot_distribution'),
    
]
    



