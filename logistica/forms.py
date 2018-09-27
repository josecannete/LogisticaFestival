# -*- coding: utf-8 -*-/
from django import forms
from logistica.models import Visita, Espacio, Tour, Horario
from django.db.models import Q

import datetime
import pytz

TIME_FLEX = 5


def add_mins(time, flex=TIME_FLEX):
    return time + datetime.timedelta(minutes=flex)


def sub_mins(time, flex=TIME_FLEX):
    return time - datetime.timedelta(minutes=flex)


def get_available_spaces(init_time, duration):
    # Debemos obtener Espacios disponibles
    # que no estén ocupados por alguna visita
    # Primero: Espacios que inicien pronto
    # y que duren <= tiempo disponible
    spaces = Espacio.objects.filter(
        horarioDisponible__inicio__lte=add_mins(init_time),
        duracion__lte=duration
    )
    print("first spaces")
    print(spaces)
    # Después, Espacios que fin de horarioDisponible
    # sea <= inicio de horarioDisponible + duracion
    spaces2 = []
    for space in spaces:
        times = space.horarioDisponible.filter(
            inicio__lte=add_mins(init_time)
        )
        for time in times:
            if time.fin >= add_mins(time.inicio, space.duracion * 0.5 + 10):
                spaces2.append(space)
                break
    print("second spaces")
    print(spaces2)
    available_spaces = []
    # Finalmente, vemos que esos espacios no estén ocupados por una visita
    for space in spaces2:
        limit_end_time = add_mins(init_time, space.duracion * 0.5 + 10)
        visits = Visita.objects.filter(
            Q(espacio=space),
            Q(horario__inicio__lte=init_time, horario__fin__gte=init_time) |
            Q(horario__inicio__lte=limit_end_time, horario__fin__gte=limit_end_time)
        ).order_by('-horario__fin')
        wait_time = 0
        while len(visits):
            new_init_time = visits[0].horario.fin
            wait_time += int((new_init_time - init_time).seconds / 60)
            limit_end_time = add_mins(new_init_time, space.duracion * 0.5 + 10)
            visits = Visita.objects.filter(
                Q(espacio=space),
                Q(horario__inicio__lte=new_init_time, horario__fin__gte=new_init_time) |
                Q(horario__inicio__lte=limit_end_time, horario__fin__gte=limit_end_time)
            ).exclude(pk=visits[0].pk).order_by('-horario__fin')
        available_spaces.append([space, wait_time])
    available_spaces.sort(key=lambda x: x[1])
    return available_spaces


class NewTourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ('nombre', 'duracion', 'alumnos')

    def __init__(self, *args, **kwargs):
        super(NewTourForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def save(self):
        super(NewTourForm, self).save(commit=False)
        # time_now = datetime.datetime.now()
        actual_time = datetime.datetime(2018, 10, 18, 13, 0, 0, 0, pytz.UTC)
        duration = self.cleaned_data['duracion']
        spaces = []
        visits = []
        while duration > 0:
            print("duration: " + str(duration))
            available_spaces = get_available_spaces(actual_time, duration)
            print("AV B4")
            print(available_spaces)
            available_spaces = [k for k in available_spaces if k[0] not in spaces]
            print("AV after")
            print(available_spaces)
            if len(available_spaces):
                info_space = available_spaces[0]
                space = info_space[0]
                wait_time = info_space[1]
                spaces.append(space)
                horario, created = Horario.objects.get_or_create(
                    inicio=add_mins(actual_time, wait_time),
                    fin=add_mins(actual_time, space.duracion + wait_time)
                )

                visit = Visita.objects.create(horario=horario, espacio=space)
                visit.save()
                visits.append(visit)

                actual_time = horario.fin
                duration -= space.duracion - wait_time
            else:
                break
        print(visits)
