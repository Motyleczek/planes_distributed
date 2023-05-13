# imports
from classes_declarations import ID
from controllers import Controller
from supervisor import Supervisor
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