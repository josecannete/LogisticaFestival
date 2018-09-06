# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from logistica.models import Actividad, Monitor, Espacio
import datetime
from .calendar import getEventsByMonitor, getEventsByEspacio


def home(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'app/home.html')
    return redirect(reverse(login_user))


def principal(request):
    if request.user.is_authenticated:
        charlas = Actividad.objects.filter(horario__inicio__gt=datetime.datetime.now(),
                                           horario__inicio__day=datetime.datetime.now().day, tipo='charla')
        talleres = Actividad.objects.filter(horario__inicio__gt=datetime.datetime.now(),
                                            horario__inicio__day=datetime.datetime.now().day, tipo='taller')
        context = {'charlas': charlas, 'talleres': talleres}
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
        monitoresDisponibles = Monitor.objects.all()
        context = {'events': getEventsByMonitor(nombreMonitor),
                   'disponibles': monitoresDisponibles
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
                print(request.POST)
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