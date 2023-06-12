# from classes.system import System
# from classes.system_generator import generate_system
# from classes.controllers import create_flight_controller
# from classes.system_generator import read_flights_data, read_planes_data

# from classes.controllers import Controller

# # Read data from CSV files
# plane_list = read_planes_data('classes/data/planes.csv')
# flight_list = read_flights_data('classes/data/flights.csv')

# # create_flight_controller(plane_list, flight_list)

# test = generate_system('classes/data')
# # system_test = System()
# create_flight_controller(plane_list, flight_list)
from classes.flight import Plane, Flight
from classes.classes_declarations import ID, Address
from classes.controllers import create_flight_controller
import threading
import time
import random

# # Import the generated plane list and flight list from system_generator.py
# from classes.system_generator import read_planes_data, read_flights_data
from classes.system_generator import generate_system
test = generate_system('classes/data')
test.simulation_start()


# # system_test = System()

# def simulate_system():
#     # Use the generated plane list and flight list
#     plane_list = test.list_of_planes
#     flight_list = test.list_of_flights

#     # Create flight controllers in separate threads
#     threads = []
#     for i in range(5):
#         thread = threading.Thread(target=create_flight_controller, args=(plane_list, flight_list))
#         threads.append(thread)
#         thread.start()

#     # Simulate communication between controllers
#     while True:
#         time.sleep(10)  # Sleep for 10 seconds

#         # Choose a random flight to update its state
#         flight_index = random.randint(0, len(flight_list) - 1)
#         flight = flight_list[flight_index]
#         flight.update()

#         # Choose a random controller to send the flight information or plane
#         controller_index = random.randint(0, len(threads) - 1)
#         controller_thread = threads[controller_index]
#         controller_id = controller_index + 1

#         if flight.close_to_leaving:
#             if flight.is_leaving:
#                 print(f"Sending plane {flight.id} from controller {controller_id}")
#                 controller_thread.controller.send_plane(flight, threads)
#             else:
#                 print(f"Sending info about plane {flight.id} from controller {controller_id}")
#                 controller_thread.controller.send_info(flight, threads)

#     # Wait for all threads to complete
#     for thread in threads:
#         thread.join()


# if __name__ == "__main__":
#     simulate_system()
