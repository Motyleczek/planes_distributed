# imports
from classes_declarations import Adress, ID
from typing import Tuple, List


# TODO
class Plane():
    def __init__(self):
        self.id: ID = None
        self.model: str = None
        self.max_speed: float = None
        self.colour: str = None
        self.engines: int = None
        self.purpose: str = None


# TODO
# each flight is different, no two planes have the same flight path, 
# therefore flight being the more important class makes sense
class Flight():
    def __init__(self):
        self.id: ID = None
        self.adress: Adress = None
        self.controller: Tuple(ID, Adress) = None
        self.flight_sector_path: List[ID] = None
        self.flight_date: str = None
        self.distance_to_next_sector: float = None
        self.plane: Plane = None
    
    # to alter route:
    def go_to(self, ID):
        pass
    
    def get_distance(self):
        return self.distance_to_next_sector
    
    def update(self, time_impulse):
        pass


