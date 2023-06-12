# imports:
from typing import Tuple, List, Optional
from classes.classes_declarations import Address, ID, UPDATE, INCOMING_PLANE, INCOMING_INFO
from classes.flight import Plane, Flight
import numpy as np
import socket
import threading
import pickle
import os
MAX_PLANES = 5


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
        self.host = socket.gethostname()
        self.port = 12340 + id
        self.socket = None
        self.connected = False
        self.connections = []
        self.plane_list: List[Plane] = plane_list
        self.max_planes: int = MAX_PLANES
        self.flight_list: List[Tuple[ID, Address]] = flight_list 
        self.flight_list_flights: List[object] = flight_list_flights # tu muszą być flights
        self.incoming_flights: List[ID] = None
        # self.sector: Sector = sector

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(10)
        print(f"Flight controller {self.id} is listening for connections...")

        while True:
            client_socket, client_address = self.socket.accept()
            print(f"Flight controller {self.id} connected to flight controller {client_address[1]}")
            self.connected = True
            self.connections.append(client_socket)

            receive_thread = threading.Thread(target=self.receive_data, args=(client_socket,))
            receive_thread.start()

    def receive_data(self, client_socket):
        while self.connected:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = pickle.loads(data)
                if type(message) is str:
                    # if we receive only info without a plane
                    print(f"Flight controller {self.id} received data: {message}")
                else:
                    text, flight_or_id = message
                    print(f"Flight controller {self.id} received command: {text}")
                    if text == UPDATE:
                        print(f"Updating controller {self.id}")
                        self.update_state()
                    if text == INCOMING_INFO:
                        print(f"Receiving info about plane {flight_or_id}")
                        if self.incoming_flights is None:
                            self.incoming_flights = [flight_or_id]
                        elif not(flight_or_id in self.incoming_flights):
                            self.incoming_flights.append(flight_or_id)
                        else:
                            print(f"I ALREADY KNOW ITS INCOMING, said controller {self.id}")
                    if text == INCOMING_PLANE:
                        print(f"Receiving flight {flight_or_id}")
                        if flight_or_id.id in self.incoming_flights:
                            self.incoming_flights.remove(flight_or_id.id)
                        else:
                            print("ALARM, PLANE WIHTOUT INFO")
                            # TODO: sending this alarm somewhere? how to send this to supervisor from this place?
                        self.flight_list.append(flight_or_id)
                        if len(self.flight_list) > self.max_planes:
                            print("ALARM, TOO MANY PLANES")
                            # TODO: sending this alarm somewhere? how to send this to supervisor from this place?
                            
            except ConnectionResetError:
                break

        self.connections.remove(client_socket)
        client_socket.close()

    def connect_to(self, remote_id):
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((self.host, 12340 + remote_id))

        self.connected = True
        self.connections.append(remote_socket)

        receive_thread = threading.Thread(target=self.receive_data, args=(remote_socket,))
        receive_thread.start()

        while self.connected:
            data = input(f"Flight controller {self.id}: ")
            message = pickle.dumps(data)
            self.broadcast(message)

        self.connections.remove(remote_socket)
        remote_socket.close()

    # TODO: zrobić tak zeby wysylac spiclowana krotke
    def broadcast(self, data):
        data_picled = pickle.dumps(data)
        for connection in self.connections:
            try:
                connection.send(data_picled)
            except ConnectionResetError:
                continue

    def disconnect(self):
        self.connected = False

    ###
    def _update_self(self):
        pass
    
    def _update_self2(self):
        pass
    ###
    
    #TODO
    # sending info to controller who will receive the plane
    def send_info(self, flight_nearing: Flight, controllers_list: List):
        """
        Function to send info about a flight which will be ready to leave in the near future, determined through update_state()
        
        Params:
        flight_nearing - Flight class object of the flight that will soon be ready to change controller
        
        Returns:
        None
        """
        new_controller_id, new_controller_address = flight_nearing.new_controller_generate(controllers_list)
  
        self.connect_to(new_controller_address)
        ####
        data = (INCOMING_INFO, flight_nearing.id)
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
        
        self.connect_to(new_controller_address)
        ####
        data = (INCOMING_PLANE, flight_over)
        data_pickled = pickle.dumps(data)
        self.broadcast(data_pickled)
        ####
        self.disconnect()
        
        # this might be causing problems, pay attention during debug
        for i, flight in enumerate(self.flight_list):
            if flight.id == flight_over.id:
                self.flight_list.pop(i)
                break  
        pass   
        
    # will use to update states after a time impulse given from outside
    def update_state(self, list_of_controllers):
        """
        Function to do updates as called through system at appropiate times
        
        Params:
        list_of_controllers: used by update flight to be able to update its controller
        
        Returns:
        none
        """
        print(f"Updating state of controller {self.id}")
        if self.flight_list is None:
            print(f"Nothing to update in controller {self.id}")
            pass
        elif len(self.flight_list) == 0:
            print(f"Nothing to update in controller {self.id}")
            pass
        
        for flight_ in self.flight_list_flights:
            flight_.update()

            print(f"Updating in controler{self.id}, flight {flight_.id}")
            if flight_.close_to_leaving:
                if flight_.is_leaving:
                    self.send_plane(flight_, list_of_controllers)
                else:
                    self.send_info(flight_, list_of_controllers)
            
            
            

# def create_flight_controller():
#     fc_id = int(input("Enter flight controller ID: "))
#     fc = Controller(fc_id)

#     thread = threading.Thread(target=fc.start)
#     thread.start()

#     while True:
#         print("1. Connect to another flight controller")
#         print("2. Send list to connected flight controllers")
#         print("3. Disconnect and exit")
#         choice = int(input("Enter your choice: "))

#         if choice == 1:
#             remote_id = int(input("Enter remote flight controller ID: "))
#             fc.connect_to(remote_id)
#         elif choice == 2:
#             message = input("Enter list to send (comma-separated values): ")
#             data_list = message.split(",")
#             fc.send_list(data_list)
#             continue
#         elif choice == 3:
#             fc.disconnect()
#             break

#         print("===================================")

#     thread.join()

def create_flight_controller(plane_list, flight_list):
    fc_id = int(input("Enter flight controller ID: "))
    fc = Controller(fc_id, plane_list, flight_list)

    thread = threading.Thread(target=fc.start)
    thread.start()

    while True:
        print("1. Connect to another flight controller")
        print("2. Send list to connected flight controllers")
        print("3. Disconnect and exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            remote_id = int(input("Enter remote flight controller ID: "))
            fc.connect_to(remote_id)
        elif choice == 2:
            message = input("Enter list to send (comma-separated values): ")
            data_list = message.split(",")
            fc.send_list(data_list)
            continue
        elif choice == 3:
            fc.disconnect()
            break

        print("===================================")

    thread.join()
# Usage example
if __name__ == "__main__":
    create_flight_controller()
    # def _make_connection(self, adress: Address):
    #     pass

    # def _close_connection(self, adress: Address):
    #     pass

    # def take_charge_of_plane(self):
    #     pass

    # def lose_charge_of_plane(self):
    #     pass

    # # why this function exists?
    # def track_neighbour(self):
    #     pass

    # def send_info(self):
    #     pass

    # def receive_info(self):
    #     pass
