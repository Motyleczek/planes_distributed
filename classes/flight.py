# imports
from classes_declarations import Address, ID
from typing import Tuple, List


# TODO
class Plane:
    def __init__(self, indx, model, max_speed, colour, engines, purpose):
        self.id: ID = indx
        self.model: str = model
        self.max_speed: float = max_speed
        self.colour: str = colour
        self.engines: int = engines
        self.purpose: str = purpose


# TODO
# each flight is different, no two planes have the same flight path, 
# therefore flight being the more important class makes sense
class Flight:
    def __init__(self, indx, path, date, plane_id):
        self.id: ID = indx
        self.adress: Address = 12340 + 50 + indx
        self.controller: Tuple[ID, Address] = None
        self.flight_sector_path: List[ID] = path
        self.flight_date: str = date
        self.distance_to_next_sector: float = None
        self.plane_id: ID = plane_id
    
    # to alter route:
    def go_to(self, ID):
        pass
    
    def get_distance(self):
        return self.distance_to_next_sector
    
    def update(self, time_impulse):
        pass


