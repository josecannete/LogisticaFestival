from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class HorarioDisponible(models.Model):
    inicio = models.DateTimeField
    fin = models.DateTimeField


class Espacio(models.Model):
    encargado = models.ForeignKey(User, on_delete=models.SET_NULL)
    nombre = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=2)
    capacidad = models.IntegerField(default=0)
    duracion = models.DurationField
    horarioDisponible = models.ForeignKey(HorarioDisponible, on_delete=models.SET_NULL)


class Monitor(models.Model):
    nombre = models.CharField(max_length=200)
    contacto = models.CharField(max_length=15)


class Disponibilidad(models.Model):
    inicio = models.DateTimeField
    fin = models.DateTimeField
    espacio = models.ForeignKey(Espacio, on_delete=models.SET_NULL)
    tamanoGrupo = models.IntegerField
    monitor = models.ForeignKey(Monitor, on_delete=models.SET_NULL)


class Charla(models.Model):
    nombre = models.CharField(max_length=200)
    inicio = models.DateTimeField
    capacidadTotal = models.IntegerField
    capacidadActual = models.IntegerField