from logistica.models import Visita
import json
import datetime


def visitaToEventforMonitor(visita):
    inicio = str(visita.horario.all()[0].inicio.isoformat())
    fin = str(visita.horario.all()[0].fin.isoformat())
    title = str(visita.espacio)

    event = {
        "title": title,
        "start": inicio,
        "end": fin
    }
    return event


def visitaToEventforEspacio(visita):
    inicio = str(visita.horario.all()[0].inicio.isoformat())
    fin = str(visita.horario.all()[0].fin.isoformat())
    title = str(visita.monitor.nombre)
    contacto = str(visita.monitor.contacto)

    event = {
        "title": title,
        "start": inicio,
        "end": fin,
        "contacto": contacto
    }
    return event


def convert_object_tour_to_event(object_tour):
    events = []
    for i in range(len(object_tour.places)):
        espacio = object_tour.places[i]
        inicio = object_tour.start_times[i].isoformat()
        fin = (object_tour.start_times[i] + datetime.timedelta(minutes=espacio.duracion)).isoformat()
        title = str(espacio)

        event = {
            "title": title,
            "start": inicio,
            "end": fin
        }
        events.append(event)
    return json.dumps(events)


def get_event_by_monitor(pk_monitor):
    visitas = Visita.objects.filter(monitor__pk=pk_monitor)
    events = []
    for visita in visitas:
        events.append(visitaToEventforMonitor(visita))
    return json.dumps(events)


def get_events_by_espacio(pk_espacio):
    visitas = Visita.objects.filter(espacio__pk=pk_espacio)
    events = []
    for visita in visitas:
        events.append(visitaToEventforEspacio(visita))
    return json.dumps(events)
