from django.urls import path
from polls import tp3, csv


urlpatterns=[
 # path("",views.index, name= "index"),
    path("csv", csv.import_csv, name="csv"),
    path("tp3", tp3.index, name= "tp3"),
    path('tp3/agesbyseason.png', tp3.ages_by_season, name='ages_by_season'),
    path('tp3/expensivesignings.png', tp3.top_10_expensive_signings, name='top 10 signings')
]