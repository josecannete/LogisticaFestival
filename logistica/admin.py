from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(HorarioDisponible)
admin.site.register(Espacio)
admin.site.register(Monitor)
admin.site.register(Disponibilidad)
admin.site.register(Charla)
