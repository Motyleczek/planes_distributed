# imports:
from typing import Tuple, List, Optional
from classes.classes_declarations import Address, ID
from classes.flight import Plane
import numpy as np

MAX_PLANES = 5


####
# TODO init for sure
class Sector:
    def __init__(self, id, has_airport, neighbours_id, neighbours_address):
        self.id: ID = id
        self.has_airport: bool = has_airport
        self.neighbours_id: Tuple[
            Optional[ID], Optional[ID], Optional[ID], Optional[ID], Optional[ID], Optional[ID]] = neighbours_id
        self.neighbours_address: Tuple[
            Optional[Address], Optional[Address], Optional[Address], Optional[Address], Optional[Address], Optional[
                Address]] = neighbours_address
        pass

    def get_neighbours(self):
        return self.neighbours_id, self.neighbours_address

    def get_neighbours_by_id(self, id: ID):
        idx = self.neighbours_id.index(id)
        return self.neighbours_id[idx], self.neighbours_address[idx]


# TODO everything here
class Controller:
    def __init__(self, id, sector):
        self.id: ID = id
        self.address: Address = None
        self.plane_list: List[Plane] = None
        self.max_planes: int = MAX_PLANES
        self.flight_list: List[Tuple[ID, Address]] = None
        self.sector: Sector = sector

    def _make_connection(self, adress: Address):
        pass

    def _close_connection(self, adress: Address):
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
