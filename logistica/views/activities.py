# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from logistica.models import Actividad, Monitor
from logistica.views.common import error_page
from logistica.views.constants import *


def activities(request):
    if not request.user.is_encargado_actividad():
        return error_page(request, ERR_NOT_AUTH)
    act = generate_activity_id_list(request.user)
    if not act:
        return error_page(request, ALERT_NO_ACTIVITIES)
    context = {
        'activities': act,
    }
    return render(request, 'app/activity.html', context)


def generate_activity_id_list(user=None):
    if user:
        return Actividad.objects.filter(monitor=user.monitor)
    else:
        return Actividad.objects.all()


def edit_activity_capacity(request):
    pk_activity = request.POST.get("id")
    ca_activity = int(request.POST.get("capacidadActual"))
    ans = {
        'status': False,
        'msg': ''
    }

    if pk_activity == -1:
        ans['msg'] = 'Escoja actividad válida'
        return JsonResponse(ans)

    activity = Actividad.objects.filter(pk=pk_activity)
    if not activity.exists():
        ans['msg'] = 'Actividad con dicho ID no existe'
        return JsonResponse(ans)

    activity = Actividad.objects.get(pk=pk_activity)
    if activity.capacidadTotal < ca_activity:
        ans['msg'] = 'No puede existir sobrecapacidad!'
        return JsonResponse(ans)

    activity.capacidadActual = ca_activity
    activity.save()
    ans['status'] = True
    return JsonResponse(ans)
