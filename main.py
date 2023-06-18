from classes.flight import Plane, Flight
from classes.classes_declarations import ID, Address

from classes.controllers import Controller
import threading
import time
import random

# # Import the generated plane list and flight list from system_generator.py
# from classes.system_generator import read_planes_data, read_flights_data
from classes.system_generator import generate_system
system_test = generate_system('classes/data')
system_test.init_server()
system_test.init_clients()
for i, elem in enumerate(system_test.controller_sockets):
    print(elem)
 