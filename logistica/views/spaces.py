# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# from logistica.forms import NewInscriptionWorkshopForm


@login_required
def workshop(request):
    context = {
        # 'inscription_workshop_form': NewInscriptionWorkshopForm()
    }
    return render(request, 'app/workshop.html', context)
