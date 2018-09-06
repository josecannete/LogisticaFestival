# -*- coding: utf-8 -*-/
from django import forms
from logistica.models import Visita, Espacio


class NewTourForm(forms.Form):
    duration = forms.IntegerField()
    students = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(NewTourForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def save(self):
        print(self.cleaned_data['duration'])
