# imports
from typing import Optional, List
from classes.classes_declarations import PLANE_WITHOUT_INFO, LOST_PLANE, TOO_MANY_PLANES, ID


#

class Alert():
    def __init__(self, type, id_of_alert_producer: ID, id_of_problem_plane: ID = 0): # Optional[PLANE_WITHOUT_INFO, LOST_PLANE, TOO_MANY_PLANES], id_of_alert_producer: ID):
        self.type: Optional[PLANE_WITHOUT_INFO, LOST_PLANE, TOO_MANY_PLANES] = type
        self.id_of_alerd_producer: ID = id_of_alert_producer
        self.id_of_problem_plane: ID = id_of_problem_plane
        self.resolved: bool = False
        
    def resolve(self):
        self.resolved = True
        
    
# assuming there is only ONE supervisor obj in system!
class Supervisor():
    def __init__(self):
        self.list_of_alerts: List[Alert] = None
       
    def add_alert(self, alert: Alert):
        if self.list_of_alerts is None:
            self.list_of_alerts = [alert]
        else:
            self.list_of_alerts.append(alert)  
     
    def see_alerts(self):
        if self.list_of_alerts is None:
            print("No alerts to show!")
        else:
            for elem in self.list_of_alerts:
                print(f"Alert type: {elem.type}, alert produced by controller with id: {elem.id_of_alerd_producer}, resolved: {elem.resolved}")
                
    def resolve_alerts(self):
        for elem in self.list_of_alerts:
            if not elem.resolved:
                elem.resolve()
                print(f"Resolved alert type: {elem.type}, produced by controller with id: {elem.id_of_alerd_producer}")
        