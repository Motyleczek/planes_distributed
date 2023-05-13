# imports 
from typing import List
from flight import Flight
from controllers import Controller, Sector

# 

# TODO could be removed depending on implementation of system_generator
class SectorsGeneral():
    pass

# TODO
class System():
    def __init__(self):
        self.list_of_flights: List[Flight] = None
        self.list_of_controllers: List[Controller] = None
        self.list_of_sectors: List[Sector] = None
        self.error_log: List[str] = None
        
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
        
        