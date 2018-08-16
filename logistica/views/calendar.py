from logistica.models import Visita
import json

def visitaToEventforMonitor(visita):
    inicio = str(visita.horarioDisponible.all()[0].inicio.isoformat())
    fin = str(visita.horarioDisponible.all()[0].fin.isoformat())
    title = str(visita.espacio)

    event = {
        "title": title,
        "start": inicio,
        "end": fin
    }
    return event

def visitaToEventforEspacio(visita):
    inicio = str(visita.horarioDisponible.all()[0].inicio.isoformat())
    fin = str(visita.horarioDisponible.all()[0].fin.isoformat())
    title = str(visita.monitor.nombre)
    contacto = str(visita.monitor.contacto)

    event = {
        "title": title,
        "start": inicio,
        "end": fin,
        "contacto" : contacto
    }
    return event

def getEventsByMonitor(nombreMonitor):
    visitas = Visita.objects.filter(monitor__nombre=nombreMonitor)
    events = []

    for visita in visitas:
        events.append(visitaToEventforMonitor(visita))

    return json.dumps(events)

def getEventsByEspacio(nombreEspacio):
    visitas = Visita.objects.filter(espacio__nombre=nombreEspacio)
    events = []

    for visita in visitas:
        events.append(visitaToEventforEspacio(visita))

    return json.dumps(events)
