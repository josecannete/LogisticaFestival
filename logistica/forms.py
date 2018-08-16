# -*- coding: utf-8 -*-/
from django import forms
from django.forms import ModelForm

from logistica.models import Actividad
from tempus_dominus.widgets import DateTimePicker

#
# class NewInscriptionActivityForm(ModelForm):
#     horaInicio = forms.DateTimeField(
#         required=True
#     )
#     horaFin = forms.DateTimeField(
#         required=True,
#         widget=DateTimePicker(
#             options={
#                 'minDate': '2018-07-01',
#                 'maxDate': '2018-10-31',
#             }
#         ),
#     )
#
#     class Meta:
#         model = Actividad
#         fields = ["nombre", "capacidadActual", "capacidadTotal"]
#
#     def __init__(self, *args, **kwargs):
#         super(NewWorkshopForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control'
#
#         self.fields['horaInicio'].widget = forms.DateTimeInput(
#             attrs={
#                 'class': 'form-control datetime-input'
#             }
#         )
