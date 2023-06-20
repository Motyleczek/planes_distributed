from classes.flight import Plane, Flight
from classes.classes_declarations import ID, Address

from classes.controllers import Controller
import threading
import time
import random

# # Import the generated plane list and flight list from system_generator.py
# from classes.system_generator import read_planes_data, read_flights_data
from classes.system_generator import generate_system
from classes.supervisor import *

dummy_alert_pwi = Alert(PLANE_WITHOUT_INFO, 4, 1)
dummy_alert_tmp = Alert(TOO_MANY_PLANES, 7, 3)
dummy_supervisor = Supervisor()
dummy_supervisor.add_alert(dummy_alert_pwi)
dummy_supervisor.add_alert(dummy_alert_tmp)

system_test = generate_system('classes/data')

# comment the line below if we dont want any artificially induced alerts in simul
system_test.supervisor = dummy_supervisor
###

system_test.init_server()
system_test.init_clients()
for i, elem in enumerate(system_test.controller_sockets):
    print(elem)
 
time.sleep(60)
print("\n \n Resolving alerts \n \n")
system_test.supervisor.resolve_alerts()

###########
#         #
#   gui   #
#         #
###########