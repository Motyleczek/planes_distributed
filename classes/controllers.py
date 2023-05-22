# imports:
from typing import Tuple, List, Optional
from classes_declarations import Address, ID, UPDATE
from flight import Plane, Flight
import numpy as np
import socket
import threading
import pickle
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
    def __init__(self, id):
        self.id = id
        self.host = socket.gethostname()
        self.port = 12340 + id
        self.socket = None
        self.connected = False
        self.connections = []
        self.plane_list: List[Plane] = None
        self.max_planes: int = MAX_PLANES
        self.flight_list: List[Tuple[ID, Address]] = None
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
                print(f"Flight controller {self.id} received data: {message}")
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

    def broadcast(self, message):
        for connection in self.connections:
            try:
                connection.send(message)
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
    def send_info(self, flight_nearing: Flight):
        new_controller_id, new_controller_address = flight_nearing.controller
        self.connect_to(new_controller_address)
        ####
        self.broadcast("TODO INFO")
        ####
        self.disconnect()
        pass
    
    #TODO
    # sending over the plane to another controller, DESTROY SAID PLANE FROM OUR FLIGHT LIST
    def send_plane(self, flight_over: Flight):
        new_controller_id, new_controller_address = flight_over.controller
        flight_over.new_controller_update()
        self.connect_to(new_controller_address)
        ####
        self.broadcast("TODO SENDING PLANE")
        ####
        self.disconnect()
        self.flight_list.pop(flight_over)   # this might be causing problems, pay attention during debug
        pass
    
    # receiving plane into our midsts:
    def receive_plane(self, flight_over: Flight):
        self.flight_list.append(flight_over)
        
    # will use to update states after a time impulse given from outside
    def update_state(self):
        print(f"Updating state of controller {self.id}")
        if self.flight_list is None:
            print(f"Nothing to update in controller {self.id}")
            pass
        elif len(self.flight_list) == 0:
            print(f"Nothing to update in controller {self.id}")
            pass
        
        for flight_ in self.flight_list:
            flight_.update()
            if flight_.close_to_leaving:
                if flight_.is_leaving:
                    self.send_plane(flight_)
                else:
                    self.send_info(flight_)
            
            
            

def create_flight_controller():
    fc_id = int(input("Enter flight controller ID: "))
    fc = Controller(fc_id)

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
