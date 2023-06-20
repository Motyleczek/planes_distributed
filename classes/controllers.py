# imports:
from typing import Tuple, List, Optional
from classes.classes_declarations import *
from classes.flight import Plane, Flight
import numpy as np
import socket
import threading
import pickle
import os
import time
import io
import time
MAX_PLANES = 5

class MyPickler(pickle.Pickler):
    def reducer_override(self, obj):
        """Custom reducer for Utils."""
        if getattr(obj, "__name__", None) == "Flight":
            return type, (obj.__name__, obj.__bases__, vars(obj))
        else:
            # For any other object, fallback to usual reduction
            return NotImplemented

####
# TODO init for sure
class Sector:
    def __init__(self, id, has_airport, neighbours_id):
        self.id: ID = id
        self.has_airport: bool = has_airport
        self.neighbours_id: Tuple[
            Optional[ID], Optional[ID], Optional[ID], Optional[ID], Optional[ID], Optional[ID]] = neighbours_id
        self.neighbours_address: Tuple[
            Optional[Address], Optional[Address], Optional[Address], Optional[Address], Optional[Address], Optional[
                Address]] = tuple([12340 + idx if idx is not None else idx for idx in neighbours_id])

    def get_neighbours(self):
        return self.neighbours_id, self.neighbours_address

    def get_neighbours_by_id(self, id: ID):
        idx = self.neighbours_id.index(id)
        return self.neighbours_id[idx], self.neighbours_address[idx]


# TODO everything here
class Controller:
    def __init__(self, id, plane_list, flight_list, flight_list_flights):
        self.id = id
        # self.host = socket.gethostname()
        self.port = 12340 + id
        # self.socket = None
        self.connected = False
        self.client_socket = None
        self.connections = []
        self.plane_list: List[Plane] = plane_list
        self.max_planes: int = MAX_PLANES
        self.flight_list: List[Tuple[ID, Address]] = flight_list 
        self.flight_list_flights: List[object] = flight_list_flights 
        self.incoming_flights: List[ID] = []
        
        # for flight updates:
        self.static_controller_list = None
    
    def set_static_controller_list(self, controller_list):
        self.static_controller_list = controller_list[:]
            

    def broadcast(self, data):
       
        self.client_socket.send(data)

        
    def receive_and_print_messages(self):
        while True:    
            # print("zbudowalismy go")
            data = self.client_socket.recv(1024)
            
            try:
                # print(data)
                message = pickle.loads(data)
            except:
                message = "founderror"             
            
            if type(message) is tuple:
                print(message)
                text, flight_or_id = message
                print(f"Flight controller {self.id} received command: {text}")
                if text == UPDATE:
                    print(f"Updating controller {self.id}")
                    self.update_state()
                    # send to server flight list and incoming flights
                    pickled_data = pickle.dumps((self.flight_list_flights, self.incoming_flights))
                    self.client_socket.send(pickled_data)


                if text == INCOMING_INFO:
                    print(f"Receiving info about plane {flight_or_id}")
                    if self.incoming_flights is None:
                        self.incoming_flights = [flight_or_id]
                    elif not(flight_or_id in self.incoming_flights):
                        self.incoming_flights.append(flight_or_id)
                    else:
                        print(f"I ALREADY KNOW ITS INCOMING, said controller {self.id}")
                if text == INCOMING_PLANE:
                    print(f"Receiving flight {flight_or_id.id}")
                    if self.incoming_flights is None:
                        print("ALARM, PLANE WIHTOUT INFO")
                    elif flight_or_id.id in self.incoming_flights:
                        self.incoming_flights.remove(flight_or_id.id)
                    else:
                        print("ALARM, PLANE WIHTOUT INFO")
                        # TODO: sending this alarm somewhere? how to send this to supervisor from this place?
                    self.flight_list.append(flight_or_id)
                    if len(self.flight_list) > self.max_planes:
                        print("ALARM, TOO MANY PLANES")
                        # TODO: sending this alarm somewhere? how to send this to supervisor from this place?        
                                   
               
            data = self.client_socket.recv(1024).decode()
            print(f"Received message: {data}")    

    def receive_updates(self):
        """
        Method goes to use after getting UPDATE trigger from system

        params:
        none
        
        returns:
        none
        """  
        while True:
            data = self.client_socket.recv(1024)
            data = pickle.loads(data)
            if type(data) is not tuple:
                raise TypeError('Sending should be done through tuples!')
            
            if data[0] == UPDATE:
                # print("Received an update from the flight controller system.")
                # print(f"Updating controller {self.id}")
                pickled_data = pickle.dumps((UPDATE, (self.flight_list_flights[:], self.incoming_flights)))
                # for elem in self.flight_list_flights:
                #     print(elem)
                self.client_socket.send(pickled_data)
                self.update_state()
                
            elif data[0] == INCOMING_INFO:
                
                flight_id, sender_id = data[1]
                self.incoming_flights.append(flight_id)
                # print(f"\n Controller {self.id} successfully received info abt flight {flight_id}")
                
            elif data[0] == INCOMING_PLANE:
                flight, sender_id = data[1]
                if flight.id not in self.incoming_flights:
                    # ALERT plane without info
                    pickled_msg = (PLANE_WITHOUT_INFO, (flight.id, self.id))
                    self.client_socket.send(pickled_data)
                    
                self.flight_list_flights.append(flight)
                print(f"Controller {self.id} successfully received flight {flight.id}")
                if flight.id in self.incoming_flights:
                    self.incoming_flights.remove(flight.id)
                if len(self.flight_list_flights) > MAX_PLANES:
                    # ALERT too many planes
                    pickled_msg = (TOO_MANY_PLANES, (flight.id, self.id))
                    self.client_socket.send(pickled_data)
           
            else:
                raise ValueError(f"No such message as {data[0]}")

   
    
    def main_socket_start(self):
        """
        Creating client socket and connecting it to the sever, creates indiviual threads with ability to send and recive messages

        params:
        none
        
        returns:
        none
        """  
        # Create a socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the flight controller system
        server_address = ('localhost', SERVER_ADDRESS)
        self.client_socket.connect(server_address)
        print("Connected to the flight controller system.")

        # Create a thread to receive updates from the flight controller system every 2 seconds
        updates_thread = threading.Thread(target=self.receive_updates, args=())
        updates_thread.start()

        # Create a thread to receive and print messages from other clients
        # messages_thread = threading.Thread(target=self.receive_and_print_messages, args=())
        # messages_thread.start()

        self.connected = True
    
    def init_socket(self):
        #initation made this way to set up client socket after server socket was set
        self.main_socket_start()
        
    def main_socket_stop(self):

        self.client_socket.close()
        self.connected = False

    def update_state(self):
        """
        Function to do updates as called through system at appropiate times
        
        Params:
        list_of_controllers: used by update flight to be able to update its controller
        
        Returns:
        none
        """
        # print(f"Updating state of controller {self.id}")
        if self.flight_list_flights is None:
            # print(f"Nothing to update in controller {self.id}")
            pass
        elif len(self.flight_list_flights) == 0:
            # print(f"Nothing to update in controller {self.id}")
            pass
        
        # for elem in self.flight_list_flights:
        #     print(elem)
        dummy_flights = []
        for flight_ in self.flight_list_flights[:]:
            flight_.update()
            print(f"Updating in controler{self.id}, flight {flight_.id}")
            time.sleep(0.5)
            if flight_.close_to_leaving or flight_.is_leaving:
                if flight_.is_leaving:
                    self.send_plane(flight_, self.static_controller_list)
                    print("sent plane", flight_)
                else:
                    dummy_flights.append(flight_)
                    self. _send_info(flight_, self.static_controller_list)
            else:
                dummy_flights.append(flight_)
        self.flight_list_flights = dummy_flights[:]
        
        
            


    
    ###
    def _update_self(self):
        pass
    
    def _update_self2(self):
        pass
    ###
    
    #TODO
    # sending info to controller who will receive the plane
    def  _send_info(self, flight_nearing: Flight, controllers_list: List):
        """
        Function to send info about a flight which will be ready to leave in the near future, determined through update_state()
        
        Params:
        flight_nearing - Flight class object of the flight that will soon be ready to change controller
        
        Returns:
        None
        """
        new_controller_id, new_controller_address = flight_nearing.new_controller_generate(controllers_list)
  
        # self.connect_to(new_controller_id)
        ####
        data = (INCOMING_INFO, (flight_nearing.id, new_controller_id))
        data_pickled = pickle.dumps(data)
        self.broadcast(data_pickled)
        ####
        self.disconnect()
        pass
    
    
    def send_plane(self, flight_over: Flight, controller_list: List):
        """
        Function to send a plane over which was deemed ready to leave our airspace through update_state()
        
        Params:
        flight_over - Flight class object of the flight that will cross over to the next controller
        
        Returns:
        None
        """
        flight_over.new_controller_update(controller_list)
        new_controller_id, new_controller_address = flight_over.controller
        if new_controller_id == self.id:
            raise ValueError("Sending plane to ourselfes, wrong!")
        
        
        ####
        data = (INCOMING_PLANE, (flight_over, new_controller_id))
        data_pickled = pickle.dumps(data)
        print(f"sending planne {flight_over.id} to controller {new_controller_id}")
        self.broadcast(data_pickled)
        ####
        
        # this might be causing problems, pay attention during debug
        for i, flight in enumerate(self.flight_list_flights[:]):
            if flight.id == flight_over.id:
                self.flight_list_flights.pop(i)
                break  
        pass   
    
    
