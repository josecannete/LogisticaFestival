from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Horario(models.Model):
    inicio = models.DateTimeField()
    fin = models.DateTimeField()


class Espacio(models.Model):
    encargado = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=2)
    capacidad = models.IntegerField(default=0)
    duracion = models.DurationField()
    horarioDisponible = models.ManyToManyField(Horario)

    def __str__(self):
        return self.nombre


class Monitor(models.Model):
    nombre = models.CharField(max_length=200)
    contacto = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre


class Reserva(models.Model):
    inicio = models.DateTimeField()
    fin = models.DateTimeField()
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE)
    tamanoGrupo = models.IntegerField()
    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE)


class Charla(models.Model):
    nombre = models.CharField(max_length=200)
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    capacidadTotal = models.IntegerField()
    capacidadActual = models.IntegerField()

    def __str__(self):
        return self.nombre


class Taller(models.Model):
    nombre = models.CharField(max_length=200)
    horario = models.DateTimeField()
    capacidadTotal = models.IntegerField()
    capacidadActual = models.IntegerField()

    def __str__(self):
        return self.nombre