# imports:
from typing import Tuple, List
from classes_declarations import Adress, ID
from flight import Plane
import numpy as np


####
# TODO init for sure
class Sector():
    def __init__(self):
        self.id: ID = None
        self.has_airport: bool = None
        self.neighbours_id: Tuple(ID) = None
        self.neighbours_adress: Tuple(Adress) = None
        pass
    
    def get_neighbours(self):
        return self.neighbours_id, self.neighbours_adress
        
    def get_neighbours_by_id(self, id: ID):
        idx = self.neighbours_id.index(id)
        return self.neighbours_id[id], self.neighbours_adress[id]


# TODO everything here
class Controller():
    def __init__(self, id: ID):
        self.id: ID = None
        self.adress: Adress = None
        self.plane_list: List[Plane] = None
        self.max_planes: int = 5
        self.flight_list: List[Tuple[ID, Adress]] = None
        self.sector: Sector = None
    
    def _make_connection(self, adress: Adress):
        pass
    
    def _close_connection(self, adress: Adress):
        pass
    
    def take_charge_of_plane(self):
        pass
    
    def lose_charge_of_plane(self):
        pass
    
    # why this function exists?
    def track_neighbour(self):
        pass
    
    def send_info(self):
        pass
    
    def receive_info(self):
        pass
    
    # will use to update states after a time impulse given from outside
    def update_state(self, time_impulse):
        pass
    
    
    
    
    
    








