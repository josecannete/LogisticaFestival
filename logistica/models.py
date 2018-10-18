from django.db import models
from django.contrib.auth.models import User


# Create your models here.
def is_monitor_stand(self):
    return self.groups.filter(name='Monitor Stand Principal').exists()


def is_monitor_tour(self):
    return self.groups.filter(name='Monitor Tour').exists()


def is_monitor_encargado(self):
    return self.groups.filter(name='Monitor Encargado').exists()


def is_monitor_informaciones(self):
    return self.groups.filter(name='Monitor Informaciones').exists()


def is_encargado_actividad(self):
    return self.groups.filter(name='Encargado Actividad').exists()


def is_encargado_espacio(self):
    return self.groups.filter(name='Encargado Espacio').exists()


def is_encargado_zona(self):
    return self.groups.filter(name='Encargado Zona').exists()


User.add_to_class("is_monitor_stand", is_monitor_stand)
User.add_to_class("is_monitor_tour", is_monitor_tour)
User.add_to_class("is_monitor_encargado", is_monitor_encargado)
User.add_to_class("is_monitor_informaciones", is_monitor_informaciones)
User.add_to_class("is_encargado_actividad", is_encargado_actividad)
User.add_to_class("is_encargado_espacio", is_encargado_espacio)
User.add_to_class("is_encargado_zona", is_encargado_zona)


class Zona(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


# Horario
# Tiene horarios (?)
class Horario(models.Model):
    inicio = models.DateTimeField()
    fin = models.DateTimeField()

    def __str__(self):
        return self.inicio.strftime("%d/%m %H:%M") + " -> " + self.fin.strftime("%H:%M")


class Monitor(models.Model):
    nombre = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contacto = models.CharField(max_length=15)

    def __str__(self):
        return str(self.nombre)

    @staticmethod
    def from_group(group):
        return Monitor.objects.filter(user__groups__name__contains=group)


class Encargado(models.Model):
    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE)
    zona = models.ManyToManyField(Zona)

    def __str__(self):
        return str(self.monitor)


# Espacio
# Contiene espacios físicos dentro de la facultad. Ej: Auditorio Gorbea
class Espacio(models.Model):
    encargado = models.ForeignKey(Monitor, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=200)
    capacidad = models.IntegerField()
    horarioAbierto = models.ManyToManyField(Horario)
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE)
    duracion = models.IntegerField()  # minutos
    observacion = models.CharField(max_length=20, blank=True)
    # TODO: sala_lugar = models.CharField(max_length=200)

    def __str__(self):
        return "{} \ zona:{}".format(str(self.nombre), str(self.zona))


# Visita
# Un tour es un conjunto de visitas
class Visita(models.Model):
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE)
    # Status indica si es tour confirmado o no. 0 si no, 1 si lo es
    status = models.IntegerField(default=0)

    def __str__(self):
        return ("Confirmado: " if self.status else "Posible: ") + str(self.espacio) + " - " + str(self.horario)


# Tour
class Tour(models.Model):
    nombre = models.CharField(max_length=200)
    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE, null=True)
    horaInicio = models.TimeField()
    duracion = models.IntegerField()
    alumnos = models.IntegerField()
    visitas = models.ManyToManyField(Visita)
    # Status indica si es tour confirmado o no. 0 si no, 1 si lo es
    status = models.IntegerField(default=0)

    def __str__(self):
        return ("Confirmado: " if self.status else "Posible: ") + self.nombre


# Actividad
# Son sólo charlas y talleres
class Actividad(models.Model):
    nombre = models.CharField(max_length=200)
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    capacidadTotal = models.IntegerField()
    capacidadActual = models.IntegerField()
    charlista = models.CharField(max_length=200, null=True, blank=True)  # Quién dara charla/taller. Sólo uso informativo
    tipo = models.CharField(max_length=15)  # Charla o taller
    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE, null=True, blank=True)
    observaciones = models.CharField(max_length=400, null=True, blank=True)
    sala_lugar = models.CharField(max_length=200, null=True, blank=True)
    contacto = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.nombre
