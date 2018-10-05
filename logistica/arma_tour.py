import copy
from random import randint
from heapq import heappush, heappop
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
    print("- available_at function")
    flex_minutes = 5
    earliest_end = init_time + datetime.timedelta(minutes=space.duracion) - datetime.timedelta(minutes=flex_minutes)
    latest_begin = init_time + datetime.timedelta(minutes=flex_minutes)
    print("earliest_end:", earliest_end)
    print("latest_begin:", latest_begin)
    # if the place is not available at this time return false
    place_is_open = False
    print("horarios espacio:", space.horarioAbierto.all())
    for block_open in space.horarioAbierto.all():
        print("Checking horario {} - {}".format(block_open.inicio, block_open.fin))
        if block_open.inicio <= latest_begin and block_open.fin >= earliest_end:
            place_is_open = True
    if not place_is_open:
        return False
    # get all the visits scheduled at this place
    visits_this_place = Visita.objects.filter(espacio=space)
    print("checking all the visits to this place")
    for visit in visits_this_place:
        # TODO: test
        # if the visit ends before my latest start time or if it starts after my earliest end time then it's ok.
        # (the negative) if it starts before my end and ends before my start then it's occupied
        print("Horario visita {} - {}".format(visit.horario.inicio, visit.horario.fin))
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
        datetime.timedelta: Estimated walking time between those Espacio's
    """
    return datetime.timedelta(minutes=10)
    # TODO: estimate an array between all groups of places
    # TODO: change 'ubicacion' on the model to be an integer that'll represent the group of the place


def is_good_route(tour_object):
    """
    Args:
        tour_object: python object Tour
    Returns:
        true if the same location is only repeated when it's in a row and not
        all the locations are the same
    """
    visited = set()
    zone_before = tour_object.places[0].zona
    visited.add(zone_before)
    for place in tour_object.places:
        this_zone = place.zona
        # different zone not already visited
        if this_zone != zone_before and this_zone not in visited:
            zone_before = this_zone
            visited.add(this_zone)
        # zone is already visited but it's not the one before
        elif this_zone != zone_before:
            return False
    # only visits one zone
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
        self.end_time = start_time + datetime.timedelta(minutes=first_place.duracion)
        self.places = [first_place]
        self.good_route = True

    def get_last_place(self):
        return self.places[-1]

    def add_place(self, new_place, start_time_new_place):
        self.start_times.append(start_time_new_place)
        self.end_time += (get_walking_time(self.get_last_place(), new_place) +
                          datetime.timedelta(minutes=new_place.duracion))
        self.places.append(new_place)

    def is_place_included(self, to_check_place):
        """Returns True if the place is already visited in this tour, if not False."""
        for place_visited in self.places:
            if to_check_place == place_visited:
                return True
        return False

    def __str__(self):
        return " -> ".join([str(p) for p in self.places])


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

    # TODO: infinite while if not enough places with my capacity

    # TODO: chequear parámetros
    print("Args:")
    print("groups_places:", groups_places)
    print("start_time:", start_time)
    print("number_people:", number_people)
    print("target_duration:", target_duration)
    print("tours_count", tours_count)

    incomplete_tours = []
    complete_tours = []
    # save 5 longest incomplete_tours in case there's no possibility for targeted_duration
    incomplete_finished_min_heap = []  # incomplete in time but finished in possibilities
    target_end_time = start_time + datetime.timedelta(minutes=target_duration)
    start_time += datetime.timedelta(minutes=10)  # time to make the tour and get the group to the first place
    # select all places that are available at the start hour
    print("Adding all possibles starts")
    for group in groups_places:
        for place in group:
            print("Checking:", place)
            if available_at(place, start_time) is not None:
                print("is available")
                incomplete_tours.append(ObjectTour(place, start_time))
    # generate all possible tours according to time constraint
    print("..Creating all possible tours, len(seeds)=", len(incomplete_tours))
    while len(incomplete_tours) > 0:
        # get first
        curr_tour = incomplete_tours.pop()
        print("curr_tour:", curr_tour)
        # already have the wanted duration, then we're done with this tour
        if curr_tour.end_time >= target_end_time:
            complete_tours.append(curr_tour)
            continue
        tour_has_next = False  # to check if the curr_tour is again added to incomplete_tours
        # create a new tour for each possible place that can go next
        for group in groups_places:
            for place in group:
                print("Checking to add place:", place)
                # if the place cannot support the amount of people ignore it
                if place.capacidad < number_people:
                    continue
                # time arriving at the new place
                next_hour = curr_tour.end_time + get_walking_time(curr_tour.get_last_place(), place)
                print("Is place already on the tour:", curr_tour.is_place_included(place))
                print("Searching place at:", next_hour)
                # if the place is not already on the tour and it's available at this time
                if not curr_tour.is_place_included(place) and available_at(place, next_hour):
                    # create new tour with that place as next
                    print("creating new tour with this stop")
                    tour_has_next = True
                    next_curr_tour = copy.deepcopy(curr_tour)
                    next_curr_tour.add_place(place, next_hour)
                    incomplete_tours.append(next_curr_tour)
        # if there's no possible next place check if this is longer than 5 incomplete finished tours
        # if the heap has space just add it
        # if it hasn't but the current tour ends later than the smaller (event that finishes earliest) add it.
        # TODO: test
        if not tour_has_next and (len(incomplete_finished_min_heap) < tours_count
                                  or curr_tour.end_time > incomplete_finished_min_heap[0][0]):
            if len(incomplete_finished_min_heap) == tours_count:
                heappop(incomplete_finished_min_heap)
            heappush(incomplete_finished_min_heap, (curr_tour.end_time, curr_tour))
    # tag tours with bad order of locations
    count_bad_locations = 0
    for tour in complete_tours:
        if not is_good_route(tour):
            print("not good route:", tour)
            count_bad_locations += 1
            tour.good_route = False
    # if possible delete tours with bad location
    print("len(complete_tours):", len(complete_tours))
    print("count_bad_locations:", count_bad_locations)
    if len(complete_tours) - count_bad_locations >= tours_count:
        complete_tours = list(filter(lambda this_tour: this_tour.good_route, complete_tours))
    # select tours to return randomly
    print("len(complete_tours):", len(complete_tours))
    if len(complete_tours) < tours_count:
        complete_tours += [tour_ for time_, tour_ in incomplete_finished_min_heap]
    for i in range(tours_count):
        selected = randint(i, len(complete_tours) - 1)
        complete_tours[i], complete_tours[selected] = complete_tours[selected], complete_tours[i]
    return complete_tours[0:tours_count]
