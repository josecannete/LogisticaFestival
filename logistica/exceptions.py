class CannotDeleteConfirmedVisitException(Exception):
    def __init__(self):
        Exception.__init__(self, "No se pueden borrar una visita ya confirmada!")


class CannotDeleteConfirmedTourException(Exception):
    def __init__(self):
        Exception.__init__(self, "No se puede borrar un tour ya confirmado!")


class NoToursAvailableException(Exception):
    def __init__(self):
        Exception.__init__(self, "No existen lugares disponibles para armar un tour con estos requerimientos")