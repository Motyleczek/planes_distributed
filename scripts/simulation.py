from classes.flight import Plane, Flight
from classes.classes_declarations import ID, Address
from classes.controllers import create_flight_controller
import threading
import time


def simulate_system():
    # Create plane and flight objects
    plane1 = Plane(1, "Boeing 747", 900, "White", 4, "Passenger")
    plane2 = Plane(2, "Airbus A320", 800, "Blue", 2, "Passenger")
    plane3 = Plane(3, "Cessna 172", 150, "Red", 1, "Private")
    plane4 = Plane(4, "Boeing 777", 1000, "White", 4, "Cargo")
    plane5 = Plane(5, "Embraer E190", 850, "Green", 2, "Passenger")

    flight1 = Flight(1, "Address1", 1, [1, 2, 3, 4], "2023-06-15", 1)
    flight2 = Flight(2, "Address2", 2, [2, 3, 4, 5], "2023-06-16", 2)
    flight3 = Flight(3, "Address3", 3, [3, 4, 5, 1], "2023-06-17", 3)
    flight4 = Flight(4, "Address4", 4, [4, 5, 1, 2], "2023-06-18", 4)
    flight5 = Flight(5, "Address5", 5, [5, 1, 2, 3], "2023-06-19", 5)

    plane_list = [plane1, plane2, plane3, plane4, plane5]
    flight_list = [flight1, flight2, flight3, flight4, flight5]

    # Create flight controllers in separate threads
    threads = []
    for i in range(5):
        thread = threading.Thread(target=create_flight_controller, args=(plane_list, flight_list))
        threads.append(thread)
        thread.start()

    # Simulate communication between controllers
    while True:
        time.sleep(10)  # Sleep for 10 seconds

        # Choose a random flight to update its state
        flight_index = random.randint(0, len(flight_list) - 1)
        flight = flight_list[flight_index]
        flight.update()

        # Choose a random controller to send the flight information or plane
        controller_index = random.randint(0, len(threads) - 1)
        controller_thread = threads[controller_index]
        controller_id = controller_index + 1

        if flight.close_to_leaving:
            if flight.is_leaving:
                print(f"Sending plane {flight.id} from controller {controller_id}")
                controller_thread.controller.send_plane(flight, threads)
            else:
                print(f"Sending info about plane {flight.id} from controller {controller_id}")
                controller_thread.controller.send_info(flight, threads)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    simulate_system()
