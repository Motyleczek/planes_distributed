import threading
# testing for now

# something like this belo will work - but we need to have a way to stop the simulation with calling .cancel()
#####
TIME_INTERVAL = 2

def printing_something():
    print(f"no elo, minęło {TIME_INTERVAL} sekund")
    t = threading.Timer(TIME_INTERVAL, printing_something)
    t.name = "state_update_thread"
    print(threading.active_count())
    print(threading.enumerate())
    t.start()

t = threading.Timer(TIME_INTERVAL, printing_something)
t.name = "state_update_thread"
t.start()
print(threading.active_count())
print(threading.enumerate())
#####

# mock function to actually play simulation
###
UPDATE_INTERVAL = 10

def simulation_run():
    # go through every controller in system
    
    # send a ping with message, lets say "UPDATE_STATE"
    
    # create a new thread with next update
    pass
    

def simulation_start(system):
    t = threading.Timer(UPDATE_INTERVAL, simulation_run, args=[])
    t.name = "update_state_thread"
    t.start()

