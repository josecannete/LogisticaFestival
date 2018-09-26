import copy
from random import randint

def available_at(space, time):
    '''
    Args:
        space Espacio
        time DateTimeField
    Returns:
        boolean, true if the space is available at that time else false.
    '''
    # TODO

def get_walking_time(from, to):
    '''
    Args:
        from Espacio
        to Espacio
    Returns:
        Estimated walking time between those Espacio's
    '''
    # TODO: estimate an array between all groups of places
    # TODO: change 'ubicacion' on the model to be an integer that'll represent the group of the place


def not_good_locations(tour):
    '''
    Args:
        tour python object Tour
    Returns:
        true if the same location is only repeated when it's in a row and not
        all the locations are the same
    '''
    visited = set()
    before = tour.places[0]
    visited.add(before)
    for place in tour.places:
        location = # TODO: get this place location
        if location != before and not in visited:
            before = location
            visited.add(location)
        elif location != before:
            return False
    if len(visited) == 1:
        return False
    return True


class Tour():
    def __init__(self, first_place):
        self.duration = #TODO: get duration of first_place
        self.places = [first_place]
        self.good_locations = True

    def get_last_place(self):
        return places[-1]

    def add_place(place):
        self.places.append(place)
        # TODO: update duration with walking time + new place duration

def get_tours(groups_places, start_time, number_people, duration=120,
              tours_count=5):
    '''
    Args:
        groups_places list of list of Espacio's
        start_time
        number_people integer
        duration integer representing minutes
        tours_count quantity of tours wanted

    Returns:
        list containing tours, each tour is a list of Espacio's
    '''

    incomplete_tours = []
    complete_tours = []
    # select all places that are available at the start hour
    for group in groups_places:
        for place in group:
            if available_at(place, start_time):
                incomplete_tours.append(Tour(place))
    # generate all posible tours according to time constraint
    while len(incomplete_tours) > 0:
        # get first
        curr_tour = incomplete_tours.pop()
        if curr_tour.duration >= duration:
            complete_tours.append(curr_tour)
            continue
        for group in groups_places:
            for place in group:
                next_hour = start_time + curr_tour.duration + get_walking_time(
                    curr_tour.get_last_place(), place)
                if available_at(place, next_hour):
                    next_curr_tour = copy.deepcopy(curr_tour)
                    next_curr_tour.add_place(place)
                    incomplete_tours.append(next_curr_tour)
    # tag tours with bad order of locations
    count_bad_locations = 0
    for tour in complete_tours:
        if not_good_locations(tour):
            count_bad_locations += 1
            tour.good_locations = False
    # if possible delete tours with bad location
    if len(complete_tours) - count_bad_locations >= tours_count:
        complete_tours = list(filter(lambda tour: tour.good_locations,
                                     complete_tours))
    # select tours to return randomly
    for i in range(tours_count):
        selected = randint(i, len(complete_tours)-1)
        tours_count[i], tours_count[selected] = (tours_count[selected],
                                                 tours_count[i])
    # TODO: return list with times for each place
    return complete_tours[0:tours_count]
