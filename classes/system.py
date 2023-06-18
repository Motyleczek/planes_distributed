# imports 
import threading
from typing import List
from classes.flight import Flight, Plane
from classes.controllers import Controller, Sector
from classes.supervisor import Supervisor, Alert
from classes.classes_declarations import SERVER_ADDRESS, UPDATE_TIME, UPDATE
import matplotlib.pyplot as plt
from datetime import date
from datetime import datetime
import os
import cv2
import socket
import pickle
import time
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
        self.thread_names = ("thr1", "thr2", "thr3", "thr4", "thr5", "thr6", "thr7")
        self.controller_sockets = None
        self.controller_threads = None
       
           
    def handle_client(self, connection, controller_id, controller_sockets):
        """
        Method used to handle messages beetwen clients

        params:
        none
        
        returns:
        none
        """  
        while True:
                             
            data = connection.recv(1024)
            data = pickle.loads(data)
            if data == "exit":
                print(f"Controller {controller_id}: Client disconnected.")
                break
            print(f"Origin Controller {controller_id}: Received message: {data}")
                       
        connection.close()
    
    def send_update_messages(self, controller_sockets):
        """
        Method used to send updates to the controllers

        params:
        none
        
        returns:
        none
        """  
        while True:
            time.sleep(UPDATE_TIME)
            for controller_socket in self.controller_sockets:
                controller_socket.send(UPDATE.encode())    


    def controller_thread(self, sock, controller_sockets):
        """
        Individual thread responsible for accepting new clients and starting thread for each of them

        params:
        none
        
        returns:
        none
        """    
        while True:
            
            # Accept a connection
            connection, client_address = sock.accept()
            print(f"Connected to: {client_address}")

            # Create a new thread to handle the controller
            controller_thread = threading.Thread(target=self.handle_client, args=(connection, len(self.controller_sockets) + 1, self.controller_sockets))
            controller_thread.start()

            # Store the controller socket
            self.controller_sockets.append(connection)
            

    def main(self):
        """
        sets up server socket and it is responsible for creating new threads for connecting clients
        Also creates lists of connected controllers

        params:
        none
        
        returns:
        none
        """
        # Create a socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to a specific address and port
        server_address = ('localhost', SERVER_ADDRESS)
        sock.bind(server_address)

        # Listen for incoming connections
        sock.listen(10)
        print("Flight controller system is now running and waiting for connections...")

        
        self.controller_threads = []
        self.controller_sockets = []

        # Create a thread for sending update messages
        update_thread = threading.Thread(target=self.send_update_messages, args=(self.controller_sockets,))
        update_thread.start()

        # Create a thread for handling controller connections
        controller_handler_thread = threading.Thread(target=self.controller_thread, args=(sock, self.controller_sockets))
        controller_handler_thread.start()

        # Might be usefull later

        # for controller_thread in controller_threads:
        #     controller_thread.join()

        # update_thread.join()
        # sock.close()
    def init_server(self):
        self.main()    
    
    def init_clients(self):
        for controller in self.list_of_controllers:
            controller.init_socket()

    def add_flight(self):
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
        
        # TODO go through sockets, not list itself
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
