from django.db import models
from django.contrib.auth.models import User

places_names = ["851_norte", "851_sur", "hall_sur", "biblioteca", "cancha", "fisica_civil", "quimica", "electrica",
                "geo"]


# Create your models here.
def is_monitor_admin(self):
    return self.groups.filter(name='Monitor Admin').exists()


def is_monitor_stand(self):
    return self.groups.filter(name='Monitor Stand Principal').exists()


def is_monitor_tour(self):
    return self.groups.filter(name='Monitor Tour').exists()


def is_encargado_actividad(self):
    return self.groups.filter(name='Encargado Actividad').exists()


def is_encargado_espacio(self):
    return self.groups.filter(name='Encargado Espacio').exists()


User.add_to_class("is_monitor_admin", is_monitor_admin)
User.add_to_class("is_monitor_stand", is_monitor_stand)
User.add_to_class("is_monitor_tour", is_monitor_tour)
User.add_to_class("is_encargado_actividad", is_encargado_actividad)
User.add_to_class("is_encargado_espacio", is_encargado_espacio)


# Horario
# Tiene horarios (?)
class Horario(models.Model):
    inicio = models.DateTimeField()
    fin = models.DateTimeField()

    def __str__(self):
        return str(self.inicio) + " -> " + str(self.fin)


class Monitor(models.Model):
    nombre = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contacto = models.CharField(max_length=15)

    def __str__(self):
        return str(self.nombre)


# Espacio
# Contiene espacios físicos dentro de la facultad. Ej: Auditorio Gorbea
class Espacio(models.Model):
    encargado = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    capacidad = models.IntegerField()
    horarioAbierto = models.ManyToManyField(Horario)
    # zonas: 851_norte, 851_sur, hall_sur, biblioteca, cancha, fisica_civil, quimica, electrica, geo
    zona = models.CharField(max_length=200)
    duracion = models.IntegerField()  # minutos

    def __str__(self):
        return str(self.nombre)



# Visita
# Un tour es un conjunto de visitas
class Visita(models.Model):
    horario = models.ManyToManyField(Horario)
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE)x


# Tour
class Tour(models.Model):
    nombre = models.CharField(max_length=200)
    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE, null=True)
    horaInicio = models.TimeField()
    duracion = models.IntegerField()
    alumnos = models.IntegerField()
    visitas = models.ManyToManyField(Visita)

    def __str__(self):
        return str(self.nombre)



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
