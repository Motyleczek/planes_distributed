# creating system from a given csv? file
# imports
from classes.flight import Plane, Flight
from classes.controllers import Sector, Controller
from classes.system import System
from typing import List

import pandas as pd


# TODO
def read_planes_data(file: str) -> List[Plane]:
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
    return planes_lst


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
        neigh_address = str(sectors_df.iloc[i]['neighbours_address'])
        neigh_address_tuple = tuple([str(el) if el != 'n' else None for el in neigh_address])
        sectors_lst.append(
            Sector(int(sectors_df.iloc[i]['id']), bool(sectors_df.iloc[i]['has_airport']), neigh_id_tuple,
                   neigh_address_tuple))
    return sectors_lst


def read_controllers_data(file: str) -> List[Controller]:
    """
    read controllers configuration from csv file and create Sectors
    :param file: path to .csv file with configuration
    :return: list of created controllers
    """
    controllers_df = pd.read_csv(file)
    controllers_lst = [Controller(int(controllers_df.iloc[i]['id']), int(controllers_df.iloc[i]['sector'])) for i in
                       range(len(controllers_df))]
    return controllers_lst


def generate_system(folder: str) -> System:
    """
    generate system based on data in files
    :param folder: path to folder with configuration files
    :return: created system
    """
    controllers = read_controllers_data(folder + '/controllers.csv')
    sectors = read_sectors_data(folder + '/sectors.csv')
    flights = read_flights_data(folder + '/flights.csv')
    planes = read_planes_data(folder + '/planes.csv')
    return System(flights, controllers, sectors, planes)


if __name__ == '__main__':
    sys = generate_system('data')