# imports
from classes.classes_declarations import ID
from classes.controllers import Controller
from classes.supervisor import Supervisor
###

# TODO
class ControllerInterface(Controller):
    def __init__(self, id):
        super().__init__(id)
        self.id: ID = id
        
# TODO       
class SupervisorInterface():
    def __init__(self):
        pass