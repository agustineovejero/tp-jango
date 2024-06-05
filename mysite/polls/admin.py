from django.contrib import admin

from polls.models import Club, Equipos, Fichaje, Persona, Temporada, Valor
# Register your models here.

admin.site.register(Persona)
admin.site.register(Fichaje)
admin.site.register(Equipos)
admin.site.register(Temporada)
admin.site.register(Valor)
admin.site.register(Club)

