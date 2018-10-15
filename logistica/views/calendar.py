from logistica.models import Visita, Tour, Espacio
import json
import datetime


def visitaToEventforMonitor(visita):
    inicio = str(visita.horario.inicio.isoformat())
    fin = str(visita.horario.fin.isoformat())
    title = str(visita.espacio)

    event = {
        "title": title,
        "start": inicio,
        "end": fin
    }
    return event


def visitaToEventforEspacio(visita, monitor, name_tour):
    inicio = str(visita.horario.inicio.isoformat())
    fin = str(visita.horario.fin.isoformat())
    name_monitor = str(monitor.nombre)
    contacto = str(monitor.contacto)

    event = {
        "title": name_tour,
        "start": inicio,
        "end": fin,
        "contacto": contacto,
        "description": name_monitor
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
    tours = Tour.objects.filter(monitor__pk=pk_monitor)
    events = []
    for tour in tours:
        visitas = tour.visitas.all()
        for visita in visitas:
            events.append(visitaToEventforMonitor(visita))
    return json.dumps(events)


def get_events_by_espacio(pk_espacio):
    tours = Tour.objects.filter(visitas__espacio__pk=pk_espacio)
    events = []
    for tour in tours:
        visita = tour.visitas.filter(espacio__pk=pk_espacio)[0]
        monitor = tour.monitor
        events.append(visitaToEventforEspacio(visita, monitor, tour.nombre))
    return json.dumps(events)


def get_events_by_tour(pk_tour):
    tour = Tour.objects.get(pk=pk_tour)
    events = []
    for visita in tour.visitas.all():
        events.append(visitaToEventforMonitor(visita))
    return json.dumps(events)


def get_name_and_events_by_espacio():
    tours = Tour.objects.all()
    espacios = Espacio.objects.all()
    espacios_id = {}
    for espacio in espacios:
        espacios_id[espacio.nombre] = []
    for tour in tours:
        visitas = tour.visitas.all()
        print("here--->", len(visitas))
        for visita in visitas:
            espacios_id[visita.espacio.nombre].append(visitaToEventforEspacio(visita, tour.monitor, tour.nombre))
    return [espacios_id.keys(), [json.dumps(events_by_espacio) for events_by_espacio in espacios_id.values()]]
