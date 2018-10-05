# -*- coding: utf-8 -*-/
from django import forms
from logistica.models import Visita, Espacio, Tour, Horario
from django.db.models import Q

import datetime
import pytz


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
