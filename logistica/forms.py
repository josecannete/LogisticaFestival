# -*- coding: utf-8 -*-/
from django import forms
from logistica.models import Visita, Espacio, Tour

import datetime


class NewTourForm(forms.ModelForm):

    class Meta:
        model = Tour
        fields = ('nombre', 'duracion', 'alumnos')

    def __init__(self, *args, **kwargs):
        super(NewTourForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def save(self):
        tour = super(NewTourForm, self).save(commit=False)
        time_now = datetime.datetime.now()