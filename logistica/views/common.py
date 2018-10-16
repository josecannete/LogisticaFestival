# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, render_to_response
from django.urls import reverse
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from logistica.arma_tour import get_tours, ObjectTour
from logistica.models import *
from logistica.forms import NewTourForm
from logistica.views.constants import *
from .calendar import get_event_by_monitor, get_events_by_espacio, get_events_by_tour, \
    convert_object_tour_to_event, visitaToEventforEspacio
from random import randint
from logistica.exceptions import *
import datetime, json


def error_404(request, exception):
    context = {
        'gif_number': str(randint(1, 4))
    }
    return render(request, 'app/404.html', context)


def error_500(request, exception):
    context = {
        'gif_number': str(randint(1, 4))
    }
    return render(request, 'app/500.html', context)


def home(request):
    user = request.user
    if user.is_authenticated:
        return redirect(reverse(principal))
    return redirect(reverse(login_user))


def error_page(request, err):
    return render(request, 'app/error_page.html', {'info': err})


def get_places_by_group():
    ans = []
    for name in places_names:
        ans.append(Espacio.objects.filter(zona__contains=name))
    return ans


def save_tour_option(request):
    if request.POST.get('select_monitor') and request.POST.get('optionTourId'):
        idMonitor = request.POST.get('select_monitor')
        idTour = request.POST.get('optionTourId')
        allIdTours = json.loads(request.POST.get('list_id_tours'))
        tour = add_to_realdb(idTour, idMonitor)
        allIdTours.remove(int(idTour))
        delete_from_fakedb(allIdTours)
        # TODO: delete day=18
        context = dict(events=get_events_by_tour(tour.pk),
                       startTime=(timezone.now().replace(day=18, hour=(tour.horaInicio.hour - 1))).strftime("%X"),
                       nameMonitor=Monitor.objects.get(pk=idMonitor).nombre)
        return render(request, 'app/showTour.html', context)
    return redirect(reverse(principal))


def delete_from_fakedb(listTourIds):
    for tour_pk in listTourIds:
        tour = Tour.objects.get(pk=tour_pk)
        if not tour.status:
            for visita in tour.visitas.all():
                if not visita.status:
                    visita.delete()
                else:
                    raise CannotDeleteConfirmedVisitException()
            tour.delete()
        else:
            raise CannotDeleteConfirmedTourException()


def add_to_realdb(optionTourId, selectedMonitorId):
    tour = Tour.objects.get(pk=optionTourId)
    tour.status = 1
    monitor = Monitor.objects.get(pk=selectedMonitorId)
    visitas = tour.visitas.all()
    for visita in visitas:
        visita.status = 1
        visita.save()
    tour.save()
    return tour


def add_to_fakedb(objectTour, nombre, alumnos):
    horaInicio = objectTour.start_times[0]
    duracion = (objectTour.end_time - horaInicio).seconds / 60
    monitor = Monitor.objects.get(pk=1)

    posible_tour = Tour.objects.create(nombre=nombre, monitor=monitor, horaInicio=horaInicio, alumnos=alumnos,
                                       duracion=duracion)

    for i in range(len(objectTour.places)):
        start_time = objectTour.start_times[i]
        end_time = start_time + datetime.timedelta(minutes=objectTour.places[i].duracion)
        horario = Horario.objects.get_or_create(inicio=start_time, fin=end_time)[0]
        posible_visita = Visita.objects.create(espacio=objectTour.places[i], horario=horario)
        posible_tour.visitas.add(posible_visita)

    return posible_tour


def create_tour_request(request):
    user = request.user
    if user.is_authenticated:
        print(request.POST)
        tour = NewTourForm(request.POST)
        tour.save()
        print(tour.cleaned_data['alumnos'])
        groups_places = get_places_by_group()
        start_time = timezone.now().replace(day=18, hour=9)  # TODO: delete replace
        number_people = tour.cleaned_data['alumnos']
        duration = tour.cleaned_data['duracion']
        tour_options = get_tours(groups_places, start_time, number_people, duration, tours_count=5)
        print("Tours seleccionados: iniciando a las {}:{}".format(start_time.hour, start_time.minute))
        print("\n\n".join(
            ["\n".join(
                ["{}/{} {}:{} - {}".format(this_time.day, this_time.month, this_time.hour, this_time.minute, space)
                 for this_time, space in zip(tour_.start_times, tour_.places)]) for tour_ in tour_options]))

        nombre = tour.cleaned_data['nombre']
        idTours = []

        for object_tour in tour_options:
            idTours.append(add_to_fakedb(object_tour, nombre, number_people).id)

        events = [convert_object_tour_to_event(tour_option) for tour_option in tour_options]
        print("LIST EVENTS:")
        print('\n'.join(events))
        context = {
            'range': range(7),
            'monitores': Monitor.from_group('Monitor Tour'),
            'idTours': idTours,
            'startTime': start_time.replace(minute=0).strftime("%X"),
            'events': events
        }
        print("CONTEXT", start_time.strftime("%X"))
        return render(request, 'app/tour.html', context)
    return redirect(reverse(login_user))


def principal(request):
    if request.user.is_authenticated:
        # start_time = datetime.datetime.now()
        start_time = timezone.now().replace(day=18, hour=12)  # TODO: Eliminar
        charlas = Actividad.objects.filter(horario__inicio__gt=start_time,
                                           horario__inicio__day=start_time.day, tipo='charla')
        talleres = Actividad.objects.filter(horario__inicio__gt=start_time,
                                            horario__inicio__day=start_time.day, tipo='taller')
        context = {
            'charlas': charlas,
            'talleres': talleres,
            'tour': NewTourForm()
        }
        return render(request, 'app/principal.html', context)
    else:
        redirect(reverse(home))


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
        events = []
        monitores = None
        # Si es monitor_stand, se permite ver listado de monitores
        if request.user.is_monitor_stand():
            events = get_event_by_monitor(pk_monitor) if pk_monitor is not None else []
            monitores = Monitor.objects.all()
        # Si es monitor tour. puede ver sólo su tour
        elif request.user.is_monitor_tour():
            events = get_event_by_monitor(request.user.monitor.pk)
        # El resto no tiene acceso
        else:
            return error_page(request, ERR_NOT_AUTH)
        context = {
            'events': events,
            'monitores': monitores,
            'pk_monitor': int(pk_monitor) if pk_monitor is not None else None
        }
        return render(request, 'app/monitor.html', context)
    else:
        return redirect(reverse(home))


def espacio(request, pk_espacio=None):
    if request.user.is_authenticated:
        events = []
        espacios = None
        # Si es monitor_stand, se permite ver listado de monitores
        if request.user.is_monitor_stand():
            events = get_events_by_espacio(pk_espacio) if pk_espacio is not None else []
            espacios = Monitor.objects.all()
        # Si es monitor tour. puede ver sólo su tour
        elif request.user.is_encargado_espacio():
            space = Espacio.objects.filter(encargado__pk=request.user.pk)
            if space.exists():
                events = get_events_by_espacio(space.all()[0].pk)
            else:
                return error_page(request, ALERT_NO_SPACES)
        # El resto no tiene acceso
        else:
            return error_page(request, ERR_NOT_AUTH)
        context = {
            'events': events,
            'espacios': Espacio.objects.all(),
            'pk_espacio': int(pk_espacio) if pk_espacio is not None else None
        }
        return render(request, 'app/espacio.html', context)
    else:
        return redirect(reverse(home))


def espacio_master(request):
    if request.user.is_authenticated:
        if request.user.is_monitor_stand():
            all_places = Espacio.objects.all()
            occupied_available_events = []
            for place in all_places:
                this_events = []
                for visit in Visita.objects.filter(espacio=place).all():
                    this_events.append({"title": "Occupied",
                                        "color": '#e9454d',
                                        "start": str(visit.horario.inicio),
                                        "end": str(visit.horario.fin)})
                for available in place.horarioAbierto.all():
                    this_events.append({"title": "Available",
                                        "color": '#84b951',
                                        "start": str(available.inicio),
                                        "end": str(available.fin)})
                occupied_available_events.append(this_events)
            context = {
                'name_places': [place.nombre for place in all_places],
                'events': occupied_available_events
            }
            print("here>", context)
            return render(request, 'app/espacio_master.html', context)
        else:
            return error_page(request, ERR_NOT_AUTH)
    else:
        return redirect(reverse(home))

# def monitorProfile(request):
#     if request.user.is_authenticated:
#         if not request.user.is_encargado_actividad():
#             return error_page(request, ERR_NOT_AUTH)
#         try:
#             if request.method == 'GET':
#                 actividades = Actividad.objects.filter(monitor=request.user.monitor)
#                 if not actividades:
#                     return error_page(request, ALERT_NO_ACTIVITIES)
#                 return render(request, 'app/profile.html', {'actividades': actividades})
#             elif request.method == 'POST':
#                 monitor_activo = request.user.monitor
#                 actividades = Actividad.objects.filter(monitor=monitor_activo)
#                 act = Actividad.objects.get(id=request.POST['actividad'])
#                 if not act:
#                     return error_page(request, ALERT_NO_ACTIVITIES)
#                 context = {
#                     'actividades': actividades,
#                     'act': act
#                 }
#                 return render(request, 'app/profile_edit.html', context)
#         except:
#             return redirect(reverse(home))
#     else:
#         return redirect(reverse(login_user))
#
#
# def updateActividad(request):
#     actividad = Actividad.objects.get(id=request.POST['id'])
#     actividad.nombre = request.POST['nombre']
#     actividad.capacidadActual = request.POST['asistentes']
#     actividad.save()
#     return redirect(reverse(monitorProfile))
