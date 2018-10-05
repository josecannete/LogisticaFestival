# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from logistica.arma_tour import get_tours, ObjectTour
from logistica.models import Actividad, Monitor, Espacio, places_names, Tour, PosibleVisita, Horario, PosibleTour
from logistica.forms import NewTourForm
import datetime
from .calendar import get_event_by_monitor, get_events_by_espacio, \
    convert_object_tour_to_event


def home(request):
    user = request.user
    if user.is_authenticated:
        return redirect(reverse(principal))
    return redirect(reverse(login_user))


def get_places_by_group():
    ans = []
    for name in places_names:
        ans.append(Espacio.objects.filter(zona__contains=name))
    return ans

def saveTourOption(request):
    print("la request es")
    print(request.POST)
    if request.POST.get('select_monitor') and request.POST.get('optionTourId'):
        idMonitor = request.POST.get('select_monitor')
        idTour = request.POST.get('optionTourId')
        tour = Tour.objects.get(idTour)
        tour.confirmado = True
        tour.monitor = Monitor.objects.get(idMonitor)
        tour.save()
        context = {}
        return render(request, 'app/showTour.html', context)
    return redirect(reverse(principal))

def add_to_fakedb(objectTour, nombre, alumnos):
    horaInicio = objectTour.start_times[0]
    duracion = objectTour.end_time - horaInicio
    monitor = Monitor.objects.get(1)

    posible_tour = PosibleTour.objects.create(nombre=nombre, monitor=monitor, horaInicio=horaInicio, alumnos=alumnos,
                               duracion=duracion, confirmado=False)

    for i in range(objectTour.places):
        start_time = objectTour.start_times[i]
        end_time = start_time + objectTour.places[i].duracion
        horario = Horario.objects.get_or_create(inicio=start_time, fin=end_time)
        posible_visita = PosibleVisita.objects.get_or_create(espacio=objectTour.places[i]).horario.add(horario)
        posible_tour.visitas.add(posible_visita)

    return posible_tour.id


def tour(request):
    user = request.user
    if user.is_authenticated:
        print(request.POST)
        tour = NewTourForm(request.POST)
        tour.save()
        print(tour.cleaned_data['alumnos'])
        groups_places = get_places_by_group()
        start_time = timezone.now().replace(day=18, hour=13)  # TODO: delete replace
        number_people = tour.cleaned_data['alumnos']
        duration = tour.cleaned_data['duracion']
        tour_options = get_tours(groups_places, start_time, number_people, duration, tours_count=5)
        print("Tours seleccionados: iniciando a las {}:{}".format(start_time.hour, start_time.minute))
        print("\n\n".join(
            ["\n".join(
                ["{}/{} {}:{} - {}".format(this_time.day, this_time.month, this_time.hour, this_time.minute, space)
                 for this_time, space in zip(tour_.start_times, tour_.places)]) for tour_ in tour_options]))

        nombre = tour.cleaned_data['nombre']
        for object_tour in tour_options:
            print(add_to_fakedb(object_tour, nombre, number_people))


        idTours = [1, 2, 3, 4, 5]
        #events = [str("[{title: 'event1',start: '2010-01-01'}]"),
        #          str("[{title: 'event2',start: '2010-01-05',end: '2010-01-07'}]"),
        #          str("[{title: 'event3',start: '2010-01-09T12:30:00',allDay: 'false'}]"),
        #          str("[{title: 'event1',start: '2010-01-01'}]"),
        #          str("[{title: 'event2',start: '2010-01-05',end: '2010-01-07'}]"),
        #          ]
        events = [convert_object_tour_to_event(tour_option) for tour_option in tour_options]
        print("LIST EVENTS:")
        print('\n'.join(events))
        context = {
            'range': range(7),
            'monitores': Monitor.objects.all(),
            'idTours': idTours,
            'events': events
        }
        return render(request, 'app/tour.html', context)
    return redirect(reverse(login_user))


def principal(request):
    if request.user.is_authenticated:
        charlas = Actividad.objects.filter(horario__inicio__gt=datetime.datetime.now(),
                                           horario__inicio__day=datetime.datetime.now().day, tipo='charla')
        talleres = Actividad.objects.filter(horario__inicio__gt=datetime.datetime.now(),
                                            horario__inicio__day=datetime.datetime.now().day, tipo='taller')
        context = {
            'charlas': charlas,
            'talleres': talleres,
            'tour': NewTourForm()
        }
        return render(request, 'app/principal.html', context)
    else:
        redirect('/')


def login_user(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me', False)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
            return redirect(reverse(home))
        else:
            context['error_login'] = 'Nombre de usuario o contraseña no válido!'
            return render(request, 'app/login.html', context)
    return render(request, 'app/login.html', context)


def logout_user(request):
    logout(request)
    return redirect(reverse(home))


def monitor(request, pk_monitor=None):
    if request.user.is_authenticated:
        context = {
            'events': get_event_by_monitor(pk_monitor),
            'monitores': Monitor.objects.all()
        }
        return render(request, 'app/monitor.html', context)
    else:
        return redirect('/')


def espacio(request, pk_espacio=None):
    if request.user.is_authenticated:
        context = {
            'events': get_events_by_espacio(pk_espacio),
            'espacios': Espacio.objects.all()
        }
        print(context)
        return render(request, 'app/espacio.html', context)
    else:
        return redirect('/')


def monitorProfile(request):
    if request.user.is_authenticated:
        try:
            if request.method == 'GET':
                context = {
                    'actividades': Actividad.objects.filter(monitor=request.user.monitor)
                }
                return render(request, 'app/profile.html', context)
            if request.method == 'POST':
                monitorActivo = request.user.monitor
                actividades = Actividad.objects.filter(monitor=monitorActivo)
                act = Actividad.objects.get(id=request.POST['actividad'])
                context = {'actividades': actividades, 'act': act}
                return render(request, 'app/profile_edit.html', context)
        except:
            return redirect('/')
    else:
        return redirect('/')


def updateActividad(request):
    actividad = Actividad.objects.get(id=request.POST['id'])
    actividad.nombre = request.POST['nombre']
    actividad.capacidadActual = request.POST['asistentes']
    actividad.save()
    return redirect('/profile/')
