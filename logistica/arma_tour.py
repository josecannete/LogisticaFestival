import copy
from random import randint
from logistica.models import Visita
import datetime


def available_at(space, time):
    """
    Args:
        space Espacio
        time DateTimeField
    Returns:
        time at which the space is available (this can differ in 5 min. from time parameter)
    """
    start_date = datetime.date(2005, 1, 1)
    end_date = datetime.date(2025, 1, 1)
    visitas = Visita.objects.filter(espacio=space).filter(horarioDisponible__inicio__range=(start_date, time)).filter(
        horarioDisponible__fin__range=(time, end_date))
    if len(visitas) > 0:
        return False
    else:
        return True
        # TODO : agregar margen de tiempo


def get_walking_time(from_place, to_place):
    """
    Args:
        from Espacio
        to Espacio
    Returns:
        Estimated walking time between those Espacio's
    """
    return 10
    # TODO: estimate an array between all groups of places
    # TODO: change 'ubicacion' on the model to be an integer that'll represent the group of the place


def not_good_route(tour):
    """
    Args:
        tour python object Tour
    Returns:
        true if the same location is only repeated when it's in a row and not
        all the locations are the same
    """
    visited = set()
    before = tour.places[0]
    visited.add(before)
    for place in tour.places:
        location = place.zona
        # different zone not already visited
        if location != before and location not in visited:
            before = location
            visited.add(location)
        # zone is already visited but it's not the one before
        elif location != before:
            return False
    if len(visited) == 1:
        return False
    return True


class ObjectTour:
    def __init__(self, first_place, start_time):
        """
        :param first_place: Espacio where the tour starts
        :param start_time: start time in the first place (the tour starting time is 5-10 minutes before)
        """
        self.start_times = [start_time]
        self.duration = first_place.duracion
        self.places = [first_place]
        self.good_route = True

    def get_last_place(self):
        return self.places[-1]

    def add_place(self, new_place, start_time_new_place):
        self.start_times.append(start_time_new_place)
        self.duration += get_walking_time(self.get_last_place(), new_place) + new_place.duracion
        self.places.append(new_place)

    def is_place_included(self, to_check_place):
        """Returns True if the place is already visited in this tour, if not False."""
        for place_visited in self.places:
            if to_check_place == place_visited:
                return True
        return False


def get_tours(groups_places, start_time, number_people, duration=120,
              tours_count=5):
    """
    Args:
        groups_places: list of list of Espacio's
        start_time: start time of the tour
        number_people: integer
        duration: integer representing minutes
        tours_count: quantity of tours wanted

    Returns:
        list of list, each list represents a tour containing tuples (time, Espacio)
    """

    # TODO: chequear parámetros
    if True:
        print(groups_places)

    incomplete_tours = []
    complete_tours = []
    start_time += 10  # time to make the tour and get the group to the first place
    # select all places that are available at the start hour
    for group in groups_places:
        for place in group:
            time_place_available = available_at(place, start_time)
            if time_place_available is not None:
                incomplete_tours.append(ObjectTour(place, time_place_available))
    # generate all possible tours according to time constraint
    while len(incomplete_tours) > 0:
        # get first
        curr_tour = incomplete_tours.pop()
        if curr_tour.duration >= duration:
            complete_tours.append(curr_tour)
            continue
        for group in groups_places:
            for place in group:
                if place.capacidad < number_people:
                    continue
                next_hour = start_time + curr_tour.duration + get_walking_time(curr_tour.get_last_place(), place)
                # the place is not already on the tour and it's available at this time
                time_place_available = available_at(place, next_hour)
                if not curr_tour.is_place_included(place) and time_place_available is not None:
                    next_curr_tour = copy.deepcopy(curr_tour)
                    next_curr_tour.add_place(place, time_place_available)
                    incomplete_tours.append(next_curr_tour)
    # tag tours with bad order of locations
    count_bad_locations = 0
    for tour in complete_tours:
        if not_good_route(tour):
            count_bad_locations += 1
            tour.good_route = False
    # if possible delete tours with bad location
    if len(complete_tours) - count_bad_locations >= tours_count:
        complete_tours = list(filter(lambda tour: tour.good_locations,
                                     complete_tours))
    # select tours to return randomly
    for i in range(tours_count):
        selected = randint(i, len(complete_tours) - 1)
        tours_count[i], tours_count[selected] = tours_count[selected], tours_count[i]
    tours_selected = complete_tours[0:tours_count]
    return [[(tour.start_times[i], place) for i, place in enumerate(tour.places)] for tour in tours_selected]
