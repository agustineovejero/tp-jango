

from django.urls import path

from polls import views


urlpatterns=[
 # path("",views.index, name= "index"),
    path("loaddatasetT", views.load_dataset, name= "load_dataset")

]