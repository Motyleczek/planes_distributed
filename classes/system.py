# imports 
import threading
from typing import List
from classes.flight import Flight, Plane
from classes.controllers import Controller, Sector
from classes.supervisor import Supervisor, Alert
import matplotlib.pyplot as plt
from datetime import date
from datetime import datetime
import os
import cv2

#

# TODO could be removed depending on implementation of system_generator
class SectorsGeneral:
    pass


# TODO
class System:
    def __init__(self, flights, controllers, sectors, planes, update_interval=10):
        self.list_of_flights: List[Flight] = flights    # this might not be updated throughout the duration of the simulation!
                                                        # use only as indication of initial states of flights, not current states
                                                        
        self.list_of_controllers: List[Controller] = controllers    # this will be updated throughout the course of simulation, thus will
                                                                    # will be used to generate visualisation
        self.list_of_sectors: List[Sector] = sectors
        self.error_log: List[str]
        self.list_of_planes: List[Plane] = planes
        self.update_interval: int = update_interval
        self.updates_done: int = 0
        self.supervisor: Supervisor = Supervisor()

    def add_flight(self):
        pass

    def generate_system(self):
        # use class from system_generate.py here if needed
        pass

    # remember to correctly close sockets
    def system_reset(self):
        pass

    # TODO
    def generate_visualisation(self):
        """
        generates visualisation png from source image simulation_map.png and saves it in simulation_visualisations folder
        saves with timestamp of when the file was saved and the simulation step at which it was saved
        
        params:
        none
        
        returns:
        none
        """
        coordinate_of_sector_on_img = {1: (360, 176),
                                        2: (180, 288),
                                        3: (360, 391),
                                        4: (560, 288),
                                        5: (180, 489),
                                        6: (360, 634),
                                        7: (560, 489)}
        coordinate_of_sector_num_on_img =  {1: (384, 133),
                                            2: (192, 219),
                                            3: (411, 315),
                                            4: (656, 210),
                                            5: (206, 427),
                                            6: (418, 534),
                                            7: (661, 583)}


        img = cv2.imread('simulation_visualisation/simulation_map.png', cv2.IMREAD_COLOR)
        scaling = 2 # percent of original size
        width = int(img.shape[1] * scaling)
        height = int(img.shape[0] * scaling)
        dim = (width, height)
  
        # resize image
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        
        for controller in self.list_of_controllers:
            x, y = coordinate_of_sector_on_img[controller.id]
            x, y = int(x*scaling), int(y*scaling)
            flight_list = []
            
            if controller.flight_list is not None:
                for flights in controller.flight_list_flights:
                    flight_list.append(flights.id)
                    
            s = 'flights ids: \n' + str(flight_list) + '\n incoming flights ids: ' + str(controller.incoming_flights)
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 0.5
            color = (255, 0, 0)
            thickness = 1
            y0, dy = y, 50
            for i, line in enumerate(s.split('\n')):
                y = y0 + i*dy
                img = cv2.putText(img, line, (x, y), font, 
                    fontScale, color, thickness, cv2.LINE_AA)
            
            
        if self.supervisor.list_of_alerts is not None:
            for alert in self.supervisor.list_of_alerts:
                x, y = coordinate_of_sector_num_on_img[alert.id_of_alerd_producer]
                x, y = int(x*scaling), int(y*scaling)
                s = '!!!'
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 255)
                thickness = 1
                y0, dy = y, 4
                for i, line in enumerate(s.split('\n')):
                    y = y0 + i*dy
                    img = cv2.putText(img, s, (x, y), font, 
                        fontScale, color, thickness, cv2.LINE_AA)
                
        my_time = datetime.min.now()
        cv2.imwrite(f"simulation_visualisations/simulation_step_{self.updates_done}_{my_time}.png", img)
        pass
        

    def see_errors(self):
        self.supervisor.see_alerts()
        
    def delete_errors(self):
        self.supervisor.resolve_alerts()
    
    # TODO: how to use this while its in threading >???
    def add_error(self, alert: Alert):
        self.supervisor.add_alert(alert)

    # for simulation, update step
    def _update(self):
        for controller_ in self.list_of_controllers:
            controller_.update_state(self.list_of_controllers)
        self.generate_visualisation()
        self.updates_done += 1
    
    def _simulation_run(self):
        t = threading.Timer(self.update_interval, self._simulation_run)
        t.name = "update_thread"
        print(f"\nContinuing updates, num. {self.updates_done}")
        self._update()
        t.start()
        
    def simulation_start(self):
        print(os.getcwd())
        for controler_ in self.list_of_controllers:
            controler_.start()
        for i, controler_ in enumerate(self.list_of_controllers):
            for j in range(7):
                if i==j: 
                    continue
                else:
                    controler_.connect_to(j+1)

        self.generate_visualisation()
        t = threading.Timer(self.update_interval, self._simulation_run)
        t.name = "update_thread"
        print("\nStarting updates:")
        self._update()
        t.start()
        
        