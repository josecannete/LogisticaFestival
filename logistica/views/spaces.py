# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from logistica.forms import NewWorkshopForm


@login_required
def workshop(request):
    context = {
        'new_workshop_form': NewWorkshopForm()
    }
    return render(request, 'app/workshop.html', context)
