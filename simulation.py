# Import necessary modules

import numpy as np
import math
import pandas as pd
import parse_data as ps
import myextrafunctionsdraft as my
import scipy
from scipy import constants
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Use function to get the DataFrame containing the information about the planets
stellar_data = ps.open_data_csv('data.csv')
stellar_data_array = stellar_data.to_numpy()
length = len(stellar_data)



def simulation_step(data, time_delta):
    """
    Computes the positions of objects after one time_delta
    :param data: a dataframe containing stellar objects' details at a certain time
    :param time_delta: time in seconds to advance positions
    :return: a dataframe containing updated data for the objects
    """
    # TODO: Your code goes here
    # Where does t = t + time_delta go?????
    positions1 = my.get_initial_position(data)
    velocities1 = my.get_initial_velocity(data)
    forces1 = my.netforces(positions1)
    accelerations1 = my.accelerations(forces1)

    # Calculate new velocity and position
    updatedvelocity = my.newvelocity(velocities1, accelerations1, time_delta)
    updatedposition = my.newposition(updatedvelocity, positions1, time_delta)
    df = pd.concat([updatedposition, updatedvelocity], axis=1)
    return df
#print(simulation_step(stellar_data,25000))


def simulate(steps, time_delta):
    """
    Loads initial positions using parse_data.open_data_csv, performs a specified amount of simulation steps with
    time_delta seconds between steps
    :param steps: number of steps to simulate
    :param time_delta: time in seconds to advance positions between steps
    :return: a dataframe containing all objects' positions at all times
    """
    # TODO: Your code goes here
    i = 0
    t = 0
    times = []
    stepscolumn = []
    namescolumn = []
    buffer = simulation_step(stellar_data, time_delta)
    t = t + time_delta
    for m in range(len(stellar_data)):
        times.append(0)
        stepscolumn.append(0)
        namescolumn.append(stellar_data['name'][m])
    for n in range(len(stellar_data)):
        times.append(t)
        stepscolumn.append(1)
        namescolumn.append(stellar_data['name'][n])

    info = []

    # create initial dataframe with info from times 0 and 25000
    df1 = my.get_initial_position(stellar_data)
    df2 = my.get_initial_velocity(stellar_data)
    time0 = pd.concat([df1, df2], axis=1)
    time1 = buffer
    chunk1 = pd.concat([time0, time1])
    #print(chunk1)

    #Had to do steps-2 because i calculated the first 2 time steps outside of the loop
    step = 1
    while i < steps-2:

        #simulation_step(buffer, time_delta)
        buffer = simulation_step(buffer, time_delta)
        t = t + time_delta
        step = step + 1
        for m in range(len(stellar_data)):
            times.append(t)
            stepscolumn.append(step)
            namescolumn.append(stellar_data['name'][m])
        info.append(buffer)
        i = i + 1

    df3 = pd.concat(info)
    finaldf = pd.concat([chunk1, df3])
    finaldf['t'] = times
    finaldf['step'] = stepscolumn
    finaldf['name'] = namescolumn
    return finaldf
simulate(100,86400)



def get_kinetic_energy(multiple_data):
    """
    Computes the kinetic energy of the system as a function of simulation step
    :param multiple_data: a DataFrame containing planet data for many steps
    :return: the kinetic energy at each step (list or numpy array)
    """
    # TODO: Your code goes here
    kenergy = []
    for index, row in multiple_data.iterrows():
        mass = stellar_data_array[index][8]
        li = [row['v_x'], row['v_y'], row['v_z']]
        vctr = np.array(li)
        magnitude = np.linalg.norm(vctr)
        kenergy.append([0.5 * mass * magnitude**2, row['t']])
    kineticenergy = np.array(kenergy)
    #print(kineticenergy)

    #Add the energy of every planet each step
    steps = len(kineticenergy) / len(stellar_data)
    new = []
    for i in range(0, int(steps)):
        new.append(my.sum_first_n_rows(kineticenergy, len(stellar_data)))
        kineticenergy = my.delete_first_n_rows(kineticenergy, len(stellar_data))
    for i in range(len(new)):
        new[i][1] = new[i][1] / len(stellar_data)
    return new



def get_potential_energy(multiple_data):
    """
    Computes the gravitational potential energy of the system as a function of simulation step
    :param multiple_data: a DataFrame containing planet data for many steps
    :return: the potential energy at each step (list or numpy array)
    """
    # TODO: Your code goes here
    ## MULTIPLICAR POR 1/2??????
    potenergy = []
    sum = 0
    flag = 0
    steps = len(multiple_data) / len(stellar_data)
    print(steps)

    while flag < steps:
        for indexi, rowi in multiple_data.head(len(stellar_data)).iterrows():
            li_i = [rowi['x'], rowi['y'], rowi['z'], rowi['t']]
            vctr_i = np.array([li_i[0], li_i[1], li_i[2]])
            for indexj, rowj in multiple_data.iterrows():
                li_j = [rowj['x'], rowj['y'], rowj['z'], rowj['t']]
                vctr_j = np.array([li_j[0], li_j[1], li_j[2]])
                if indexi != indexj and li_i[3] == li_j[3]:
                    mi = stellar_data_array[indexi][8]
                    mj = stellar_data_array[indexj][8]
                    Rji = vctr_j - vctr_i
                    magnitude = np.linalg.norm(Rji)
                    V = (-scipy.constants.G * mi * mj) / magnitude
                    sum = sum + V
                else:
                    continue
        potenergy.append([(1 / 2) * sum, rowi['t']])
        multiple_data = multiple_data.iloc[length:, :]
        sum = 0
        flag = flag + 1


    potentialenergy = np.array(potenergy)
    return potentialenergy


def get_total_energy(multiple_data):
    """
    Computes the total energy of the system as a function of simulation step
    :param multiple_data: a DataFrame containing planet data for many steps
    :return: the total energy at each step (list or numpy array)
    """
    # TODO: Your code goes here
    kinetic = get_kinetic_energy(multiple_data)
    print('kinetic', kinetic)
    potential = get_potential_energy(multiple_data)
    print('potential', potential)
    total = []

    for i in range(0, len(kinetic)):
        energy = [kinetic[i][0] + potential[i][0], kinetic[i][1]]
        total.append(energy)
    total = np.array(total)
    print(len(total))
    return total


def get_sun_distances(multiple_data, planet_name):
    """
    Computes the distance of a planet from the sun as a function of time
    :param multiple_data: object data returned from simulate
    :param planet_name: the name of the planet to find distances from the sun (a string)
    :return: list/array of distances of the planet from the sun (at different times)
    """
    # TODO: Your code goes here
    liplanet = []
    lisun = []
    planetsindex = my.find_index_for_planetname(planet_name)
    sunsindex = my.find_index_for_planetname('sun')

    for index, row in multiple_data.iterrows():
        if index == planetsindex:
            li1 = [row['x'], row['y'], row['z']]
            magnitude = np.linalg.norm(np.array(li1))
            li1 = [magnitude, row['t']]
            vctr1 = np.array(li1)
            liplanet.append(vctr1)

    for index, row in multiple_data.iterrows():
        if index == sunsindex:
            li2 = [row['x'], row['y'], row['z']]
            magnitude = np.linalg.norm(np.array(li2))
            li2 = [magnitude, 0]
            vctr2 = np.array(li2)
            lisun.append(vctr2)

    result = abs(np.array(lisun) - np.array(liplanet))
    #df = pd.DataFrame(result, columns=['x', 'y', 'z', 't'])
    return result

#get_sun_distances(simulate(700,86400), 'earth')


def get_orbit_period(sun_distances):
    """
    Estimates the orbital period (in simulation steps) of a planet from the time series of distances from the sun
    :param sun_distances: a list of distances from the sun (as a function of time)
    :return: the estimated period of the motion
    """
    # TODO: Your code goes here
    dfsundistances = pd.DataFrame(sun_distances, columns=['sundistance', 't'])
    x = dfsundistances.sundistance
    peaks, _ = find_peaks(x, height=0)
    period = peaks[1] - peaks[0]
    plt.plot(x)
    plt.plot(peaks, x[peaks], "x")
    plt.plot(np.zeros_like(x), "--", color="gray")
    plt.show()
    return period
#get_orbit_period(get_sun_distances(simulate(1000,86400),'mars'))


if __name__ == "__main__":
    data = simulate(365)
    get_potential_energy(data)
