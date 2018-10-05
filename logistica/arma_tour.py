import copy
from random import randint
from logistica.models import Visita, Espacio, Tour, Horario
import datetime


def available_at(space, init_time):
    """
    Args:
        space: Espacio
        init_time: DateTimeField
    Returns:
        time at which the space is available (this can differ in 5 min. from time parameter)
    """
    flex_minutes = 5
    earliest_end = init_time + space.duracion - datetime.timedelta(flex_minutes)
    latest_begin = init_time + datetime.timedelta(flex_minutes)
    # if the place is not available at this time return false
    if space.horarioAbierto.inicio > latest_begin or space.horarioAbierto.fin < earliest_end:
        return False
    # get all the visits scheduled at this place
    visits_this_place = Visita.objects.filter(espacio=space)
    for visit in visits_this_place:
        # if the visit ends before my latest start time or if it starts after my earliest end time then it's ok.
        # (the negative) if it starts before my end and ends before my start then it's occupied
        if not (visit.horario.fin <= latest_begin or
                visit.horario.inicio >= earliest_end):
            return False
    return True

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
        Args:
            first_place: Espacio where the tour starts
            start_time: start time in the first place (the tour starting time is 5-10 minutes before)
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


def get_tours(groups_places, start_time, number_people, target_duration=120,
              tours_count=5):
    """
    Args:
        groups_places: list of list of Espacio's
        start_time: start time of the tour
        number_people: integer
        target_duration: integer representing minutes
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
            if available_at(place, start_time) is not None:
                incomplete_tours.append(ObjectTour(place, start_time))
    # generate all possible tours according to time constraint
    while len(incomplete_tours) > 0:
        # get first
        curr_tour = incomplete_tours.pop()
        # already have the wanted duration, then we're done with this tour
        if curr_tour.duration >= target_duration:
            complete_tours.append(curr_tour)
            continue
        # create a new tour for each possible place that can go next
        for group in groups_places:
            for place in group:
                # if the place cannot support the amount of people ignore it
                if place.capacidad < number_people:
                    continue
                # time arriving at the new place
                next_hour = start_time + curr_tour.duration + get_walking_time(curr_tour.get_last_place(), place)
                # if the place is not already on the tour and it's available at this time
                if not curr_tour.is_place_included(place) and available_at(place, next_hour):
                    # create new tour with that place as next
                    next_curr_tour = copy.deepcopy(curr_tour)
                    next_curr_tour.add_place(place, next_hour)
                    incomplete_tours.append(next_curr_tour)
    # tag tours with bad order of locations
    count_bad_locations = 0
    for tour in complete_tours:
        if not_good_route(tour):
            count_bad_locations += 1
            tour.good_route = False
    # if possible delete tours with bad location
    if len(complete_tours) - count_bad_locations >= tours_count:
        complete_tours = list(filter(lambda this_tour: this_tour.good_route, complete_tours))
    # select tours to return randomly
    for i in range(tours_count):
        selected = randint(i, len(complete_tours) - 1)
        complete_tours[i], complete_tours[selected] = complete_tours[selected], complete_tours[i]
    tours_selected = complete_tours[0:tours_count]
    return [[tuple_time_place for tuple_time_place in zip(tour.start_times, tour.places)] for tour in tours_selected]
