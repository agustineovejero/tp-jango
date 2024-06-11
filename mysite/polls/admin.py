from django.contrib import admin

from polls.models import Club,Player,Signing
# Register your models here.

admin.site.register(Player)
admin.site.register(Signing)
admin.site.register(Club)

