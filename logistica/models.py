from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# Horario
# Tiene horarios (?)
class Horario(models.Model):
    inicio = models.DateTimeField()
    fin = models.DateTimeField()

    def __str__(self):
        return str(self.inicio) + " -> " + str(self.fin)


# Espacio
# Contiene espacios físicos dentro de la facultad. Ej: Auditorio Gorbea
class Espacio(models.Model):
    encargado = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    capacidad = models.IntegerField()
    horarioDisponible = models.ManyToManyField(Horario)
    # zonas: 851_norte, 851_sur, hall_sur, biblioteca, cancha, fisica_civil, quimica, electrica, geo
    #zona = models.CharField(max_length=200)
    #duracion = models.IntegerField()  # minutos

    def __str__(self):
        return str(self.nombre)


class Monitor(models.Model):
    nombre = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contacto = models.CharField(max_length=15)

    def __str__(self):
        return str(self.nombre)


# Tour
# Útil para permitir desarmar tour si no es seleccionado
class Tour(models.Model):
    nombre = models.CharField(max_length=200)
    duracion = models.IntegerField()
    alumnos = models.IntegerField()


# Visita
# Un tour es un conjunto de visitas
class Visita(models.Model):
    horarioDisponible = models.ManyToManyField(Horario)
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE)
    tamanoGrupo = models.IntegerField()
    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)


# Actividad
# Son sólo charlas y talleres
class Actividad(models.Model):
    nombre = models.CharField(max_length=200)
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    capacidadTotal = models.IntegerField()
    capacidadActual = models.IntegerField()
    charlista = models.CharField(max_length=200, null=True,
                                 blank=True)  # Quién dara charla/taller. Sólo uso informativo
    tipo = models.CharField(max_length=15)  # Charla o taller
    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
