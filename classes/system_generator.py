# creating system from a given csv file
# imports
from classes.classes_declarations import ID
from classes.flight import Plane, Flight
from classes.controllers import Sector, Controller
from classes.system import System
from typing import List, Dict, Tuple

import pandas as pd


# TODO
def read_planes_data(file: str) -> Tuple[List[Plane], List[ID]]:
    """
    read planes configuration from file and create Planes
    :param file: path to .csv file with configuration
    :return: list of created planes
    """
    planes_df = pd.read_csv(file)
    planes_lst = [
        Plane(int(planes_df.iloc[i]['indx']), str(planes_df.iloc[i]['model']), float(planes_df.iloc[i]['max_speed']),
              str(planes_df.iloc[i]['colour']), int(planes_df.iloc[i]['engines']), str(planes_df.iloc[i]['purpose']))
        for i in range(len(planes_df))]
    return planes_lst, list(planes_df['indx'])


def read_flights_data(file: str) -> List[Flight]:
    """
    read flights configuration from csv file and create Flights
    :param file: path to .csv file with configuration
    :return: list of created flights
    """
    flights_df = pd.read_csv(file)
    flights_lst = []
    for i in range(len(flights_df)):
        path = str(flights_df.iloc[i]['path'])
        path_lst = [int(el) for el in path]
        flights_lst.append(Flight(int(flights_df.iloc[i]['indx']), path_lst, str(flights_df.iloc[i]['date']),
                                  int(flights_df.iloc[i]['plane'])))
    return flights_lst


def read_sectors_data(file: str) -> List[Sector]:
    """
    read sectors configuration from csv file and create Sectors
    :param file: path to .csv file with configuration
    :return: list of created sectors
    """
    sectors_df = pd.read_csv(file)
    sectors_lst = []
    for i in range(len(sectors_df)):
        neigh_id = str(sectors_df.iloc[i]['neighbours_id'])
        neigh_id_tuple = tuple([int(el) if el != 'n' else None for el in neigh_id])
        sectors_lst.append(
            Sector(int(sectors_df.iloc[i]['id']), bool(sectors_df.iloc[i]['has_airport']), neigh_id_tuple))
    return sectors_lst


def generate_system(folder: str) -> System:
    """
    generate system based on data in files
    :param folder: path to folder with configuration files
    :return: created system
    """

    sectors = read_sectors_data(folder + '/sectors.csv')
    flights = read_flights_data(folder + '/flights.csv')
    planes, planes_id = read_planes_data(folder + '/planes.csv')
    controllers_flights_dict = {s.id: ([], [], []) for s in sectors}  # start flight and plane
    for f in flights:
        sector = f.flight_sector_path[0]
        indx = planes_id.index(f.plane_id)
        plane = planes[indx]
        controllers_flights_dict[sector][0].append(plane)
        controllers_flights_dict[sector][1].append((f.id, f.id + 12340 + 50))
        controllers_flights_dict[sector][2].append(f)
    controllers = [Controller(s.id, controllers_flights_dict[s.id][0], controllers_flights_dict[s.id][1], controllers_flights_dict[s.id][2]) for s in sectors]
    controllers_copy = controllers[:]
    for elem in controllers:
        elem.set_static_controller_list(controllers_copy)
    return System(flights, controllers, sectors, planes)


if __name__ == '__main__':
    sys = generate_system('data')
    print('success')
