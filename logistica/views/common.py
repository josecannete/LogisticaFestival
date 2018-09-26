# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from logistica.arma_tour import get_tours
from logistica.models import Actividad, Monitor, Espacio, places_names
from logistica.forms import NewTourForm
import datetime
from .calendar import getEventsByMonitor, getEventsByEspacio


def home(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'app/home.html')
    return redirect(reverse(login_user))


def get_places_by_group():
    ans = []
    for name in places_names:
        ans.append(Espacio.objects.filter(zona__contains=name))
    return ans


def tour(request):
    user = request.user
    if user.is_authenticated:
        tour = NewTourForm(request.POST)
        tour.is_valid()
        tour.save()
        groups_places = get_places_by_group()
        start_time = datetime.datetime.now()
        number_people = tour.cleaned_data['alumnos']
        duration = tour.cleaned_data['duracion']
        tours_disponibles = get_tours(groups_places, start_time, number_people, duration, tours_count=5)
        context = {'tours_disponibles' : tours_disponibles}
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


def monitor(request, nombreMonitor):
    if request.user.is_authenticated:
        context = {
            'events': getEventsByMonitor(nombreMonitor),
            'disponibles': Monitor.objects.all()
        }
        return render(request, 'app/monitor.html', context)
    else:
        return redirect('/')


def espacio(request, nombreEspacio):
    if request.user.is_authenticated:
        espaciosDisponibles = Espacio.objects.all()
        context = {'events': getEventsByEspacio(nombreEspacio),
                   'disponibles': espaciosDisponibles
                   }
        return render(request, 'app/espacio.html', context)
    else:
        return redirect('/')


def monitorProfile(request):
    if request.user.is_authenticated:
        try:
            if request.method == 'GET':
                monitorActivo = request.user.monitor
                actividades = Actividad.objects.filter(monitor=monitorActivo)
                context = {'actividades': actividades}
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
