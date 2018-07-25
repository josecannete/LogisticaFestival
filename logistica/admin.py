from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Horario)
admin.site.register(Espacio)
admin.site.register(Monitor)
admin.site.register(Reserva)
admin.site.register(Charla)
admin.site.register(Taller)