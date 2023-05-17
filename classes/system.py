# imports 
from typing import List
from classes.flight import Flight, Plane
from classes.controllers import Controller, Sector


#

# TODO could be removed depending on implementation of system_generator
class SectorsGeneral:
    pass


# TODO
class System:
    def __init__(self, flights, controllers, sectors, planes):
        self.list_of_flights: List[Flight] = flights
        self.list_of_controllers: List[Controller] = controllers
        self.list_of_sectors: List[Sector] = sectors
        self.list_of_planes: List[Plane]
        self.error_log: List[str] = planes

    def add_flight(self):
        pass

    def generate_system(self):
        # use class from system_generate.py here if needed
        pass

    # remember to correctly close sockets
    def system_reset(self):
        pass

    def generate_visualisation(self):
        pass

    def delete_error(self):
        pass
