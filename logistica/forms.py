# -*- coding: utf-8 -*-/
from django import forms
from django.forms import ModelForm

from logistica.models import Taller
from tempus_dominus.widgets import DateTimePicker


class NewWorkshopForm(ModelForm):
    horaInicio = forms.DateTimeField(
        required=True,
        widget=DateTimePicker(
            options={
                'minDate': '2018-07-01',
                'maxDate': '2018-10-31',
            }
        ),
    )
    horaFin = forms.DateTimeField(
        required=True,
        widget=DateTimePicker(
            options={
                'minDate': '2018-07-01',
                'maxDate': '2018-10-31',
            }
        ),
    )

    class Meta:
        model = Taller
        fields = ["nombre", "capacidadActual", "capacidadTotal"]

    def __init__(self, *args, **kwargs):
        super(NewWorkshopForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
