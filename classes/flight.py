# imports
import time
from classes.classes_declarations import Address, ID, SECTOR_DISTANCE
# from classes.controllers import Controller
from typing import Tuple, List
from datetime import datetime



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
        self.controller: Tuple[ID, Address] = (path[0], path[0] + 12340)
        self.flight_sector_path: List[ID] = path
        self.flight_date: str = date
        self.plane_id: ID = plane_id
        
        self.num_of_sector: int = 0
        self.current_sector_id: ID = path[0]
        self.next_sector_id: ID = path[1]
        
        #TODO#
        # this could be changed to make the planes update faster or slower etc #
        self.speed = 4 #thingies per second
        ######
        self.distance_to_next_sector: float = SECTOR_DISTANCE
        self.current_distance_to_next_sector: float = SECTOR_DISTANCE
        self.close_to_border_dist: float = self.distance_to_next_sector * 0.1
        self.close_to_leaving_dist: float = 0
        self.close_to_leaving: bool = False
        self.is_leaving: bool = False
        
        
        self.last_update_time: datetime = time.time()

    def __str__(self):
        return f'ID: {self.id}, Controller: {self.controller}, Distance to next sector: {self.distance_to_next_sector}, Next sector: {self.next_sector_id}'
       
        
    # to alter route:
    def go_to(self, ID):
        raise NotImplementedError()
    
    def get_distance(self):
        return self.distance_to_next_sector
    
    def new_controller_generate(self, list_of_controllers: List[object]) -> Tuple[ID, Address]:
        """
        used in send_info, to get the appropriate controller to send the info to WITHOUT changing the current controller of 
        flight
        
        params: 
        list_of_controllers - list of controllers in system, type Controller
        
        returns:
        controller - tuple(ID, Adress) of said controller
        """
        
        list_of_controllers_copy = list_of_controllers.copy()
        
        # if self.next_sector_id == 0:
        #     self.next_sector_id = self.flight_sector_path[0]
        
        for controller in list_of_controllers_copy:
            if controller.id == self.next_sector_id:
                controller = (self.next_sector_id, controller.port)
                break
        
        return controller
        
        
    def new_controller_update(self, list_of_controllers: List[object]):
        """
        funcitn to update controller and sector of the current flight
        
        params:
        list_of_controllers - list of Controllers passed from system, type Controller
        
        returns:
        none
        """
        list_of_controllers_copy = list_of_controllers.copy()
        
        self.num_of_sector += 1
        try:
            self.current_sector_id = self.flight_sector_path[self.num_of_sector]
        except:
            self.num_of_sector = 0
            self.current_sector_id = self.flight_sector_path[self.num_of_sector]
        
        ### tu jest problem 
        try:
            self.next_sector_id = self.flight_sector_path[self.num_of_sector + 1]
        except:
            self.next_sector_id = 0
        ###
            
        for controller in list_of_controllers_copy:
            if controller.id == self.current_sector_id:
                self.controller = (self.current_sector_id, controller.port)
                break
        
        self.current_distance_to_next_sector = SECTOR_DISTANCE + self.current_distance_to_next_sector
        
        
        
    def update(self):
        """
        Funciton to update state of flight
        
        Params:
        none
        
        returns:
        None
        """
        current_time = time.time()
        time_elapsed = current_time - self.last_update_time
        distance_travelled = time_elapsed * self.speed
        self.current_distance_to_next_sector -= distance_travelled
        if self.current_distance_to_next_sector <= self.close_to_border_dist:
            self.close_to_leaving = True
            if self.current_distance_to_next_sector <= self.close_to_leaving_dist:
                self.is_leaving = True
                
        self.last_update_time = time.time()


