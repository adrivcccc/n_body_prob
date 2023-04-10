# Import necessary modules

import numpy as np
import pandas as pd
import parse_data as ps
import myextrafunctionstrash

# Use function to get the DataFrame containing the information about the planets
stellar_data = ps.open_data_csv('data.csv')


def simulation_step(data, time_delta):
    """
    Computes the positions of objects after one time_delta
    :param data: a dataframe containing stellar objects' details at a certain time
    :param time_delta: time in seconds to advance positions
    :return: a dataframe containing updated data for the objects
    """
    # TODO: Your code goes here
    stellar_data_array = data.to_numpy()
    forces = myextrafunctions.totalforces()
    accelerations = myextrafunctions.accelerations(forces)
    xexpectations = []
    vexpectations = []
    for i in range(0, 9):
        xi = myextrafunctions.positionvector(i)
        vi = myextrafunctions.velocityvector(i)
        xexpectations.append(xi + vi * time_delta)
        vexpectations.append(vi + accelerations[i] * time_delta)
    df = pd.DataFrame({'x': xexpectations, 'v': vexpectations})
    return df

print('updated positionsss', simulation_step(stellar_data, 2))




def simulate(steps, time_delta):
    """
    Loads initial positions using parse_data.open_data_csv, performs a specified amount of simulation steps with
    time_delta seconds between steps
    :param steps: number of steps to simulate
    :param time_delta: time in seconds to advance positions between steps
    :return: a dataframe containing all objects' positions at all times
    """
    # TODO: Your code goes here
    xexpectations = simulation_step(stellar_data, time_delta)
    return 0
#simulate(5,1)


def get_kinetic_energy(multiple_data):
    """
    Computes the kinetic energy of the system as a function of simulation step
    :param multiple_data: a DataFrame containing planet data for many steps
    :return: the kinetic energy at each step (list or numpy array)
    """
    # TODO: Your code goes here
    pass


def get_potential_energy(multiple_data):
    """
    Computes the gravitational potential energy of the system as a function of simulation step
    :param multiple_data: a DataFrame containing planet data for many steps
    :return: the potential energy at each step (list or numpy array)
    """
    # TODO: Your code goes here
    pass


def get_total_energy(multiple_data):
    """
    Computes the total energy of the system as a function of simulation step
    :param multiple_data: a DataFrame containing planet data for many steps
    :return: the total energy at each step (list or numpy array)
    """
    # TODO: Your code goes here
    pass


def get_sun_distances(multiple_data, planet_name):
    """
    Computes the distance of a planet from the sun as a function of time
    :param multiple_data: object data returned from simulate
    :param planet_name: the name of the planet to find distances from the sun (a string)
    :return: list/array of distances of the planet from the sun (at different times)
    """
    # TODO: Your code goes here
    pass


def get_orbit_period(sun_distances):
    """
    Estimates the orbital period (in simulation steps) of a planet from the time series of distances from the sun
    :param sun_distances: a list of distances from the sun (as a function of time)
    :return: the estimated period of the motion
    """
    # TODO: Your code goes here
    pass


if __name__ == "__main__":
    data = simulate(365)
    get_potential_energy(data)
