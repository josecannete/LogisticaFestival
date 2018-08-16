# -*- coding: utf-8 -*-/
from django import forms
from django.forms import ModelForm

from logistica.models import Actividad


class EditCapacityActivityForm(ModelForm):
    class Meta:
        model = Actividad
        fields = ["id", "capacidadActual"]

    def __init__(self, *args, **kwargs):
        super(EditCapacityActivityForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'