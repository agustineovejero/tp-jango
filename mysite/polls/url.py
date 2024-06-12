

from django.urls import path

from polls import views


urlpatterns=[
 # path("",views.index, name= "index"),
    path("load_datasetT", views.load_dataset, name= "load_datasetT"),
    path("graph" , views.graph, name= "graph")

]