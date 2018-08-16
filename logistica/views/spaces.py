# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core import serializers

from logistica.forms import EditCapacityActivityForm
from logistica.models import Actividad


@login_required
def activities(request):
    context = {
        'capacity_activity_form': EditCapacityActivityForm(),
        'activities': generateActivityIdList()
    }
    return render(request, 'app/activity.html', context)


def generateActivityIdList():
    all_activities = Actividad.objects.all()
    ans = [{
        "id": -1,
        "nombre": "---------------------",
        "tipo": "",
        "capacidadActual": 0,
        "capacidadTotal": 0
    }]
    for activity in all_activities:
        ans.append({
            "id": activity.id,
            "nombre": activity.nombre,
            "tipo": activity.tipo.capitalize(),
            "capacidadActual": activity.capacidadActual,
            "capacidadTotal": activity.capacidadTotal,
        })
    return ans
