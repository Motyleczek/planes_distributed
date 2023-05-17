# imports 
import threading
from typing import List
from classes.flight import Flight, Plane
from classes.controllers import Controller, Sector
#

# TODO could be removed depending on implementation of system_generator
class SectorsGeneral:
    pass


# TODO
class System:
    def __init__(self, flights, controllers, sectors, planes, update_interval=10):
        self.list_of_flights: List[Flight] = flights
        self.list_of_controllers: List[Controller] = controllers
        self.list_of_sectors: List[Sector] = sectors
        self.list_of_planes: List[Plane]
        self.error_log: List[str] = planes
        self.update_interval: int = update_interval

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

    # for simulation, update step
    def _update(self):
        print("doing update")
        pass
    
    def _simulation_run(self):
        t = threading.Timer(self.update_interval, self._simulation_run)
        t.name = "update_thread"
        self._update()
        t.start()
        
    def simulation_start(self):
        t = threading.Timer(self.update_interval, self._simulation_run)
        t.name = "update_thread"
        self.update()
        t.start()