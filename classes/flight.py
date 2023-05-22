# imports
import time
from classes.classes_declarations import Address, ID, SECTOR_DISTANCE
from typing import Tuple, List, datetime



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
        self.plane_id: ID = plane_id
        
        self.num_of_sector: int = 0
        self.current_sector_id: ID = path[0]
        self.next_sector_id: ID = path[1]
        
        #TODO#
        self.speed = 4 #thingies per second
        ######
        self.distance_to_next_sector: float = SECTOR_DISTANCE
        self.current_distance_to_next_sector: float = SECTOR_DISTANCE
        self.close_to_border_dist: float = self.distance_to_next_sector * 0.1
        self.close_to_leaving_dist: float = 0
        self.close_to_leaving: bool = False
        self.is_leaving: bool = False
        
        
        self.last_update_time: datetime = time.time()

       
        
    # to alter route:
    def go_to(self, ID):
        pass
    
    def get_distance(self):
        return self.distance_to_next_sector
    
    def new_controller_update(self):
        self.num_of_sector += 1
        try:
            self.current_sector_id = self.flight_sector_path[self.num_of_sector]
        except:
            self.num_of_sector = 0
            self.current_sector_id = self.flight_sector_path[self.num_of_sector]
        
        try:
            self.next_sector_id = self.flight_sector_path[self.num_of_sector + 1]
        except:
            self.next_sector_id = 0
        
        self.current_distance_to_next_sector = SECTOR_DISTANCE + self.current_distance_to_next_sector
        
        
        
    def update(self):
        current_time = time.time()
        time_elapsed = current_time - self.last_update_time
        distance_travelled = time_elapsed * self.speed
        self.current_distance_to_next_sector -= distance_travelled
        if self.current_distance_to_next_sector <= self.close_to_border_dist:
            self.close_to_leaving = True
            if self.current_distance_to_next_sector <= self.close_to_leaving_dist:
                self.is_leaving = True
        self.last_update_time = time.time()


