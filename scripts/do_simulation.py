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

