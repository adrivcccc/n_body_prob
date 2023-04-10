import numpy as np
import pandas as pd
import parse_data as ps
import scipy
from scipy import constants


# Use function to get the DataFrame containing the information about the planets
stellar_data = ps.open_data_csv('data.csv')

# Convert stellar_data from a DataFrame to an numpy 2D array
stellar_data_array = stellar_data.to_numpy()

def get_initial_position(data):
    initial = []
    for i in range(len(stellar_data)):
        positions = [data.loc[i].at['x'], data.loc[i].at['y'], data.loc[i].at['z']]
        vctr = np.array(positions)
        initial.append(vctr)
    df = pd.DataFrame(initial, columns=['x', 'y', 'z'])
    return df
#print(get_initial_position(stellar_data))

def get_initial_velocity(data):
    initial = []
    for i in range(len(stellar_data)):
        velocities = [data.loc[i].at['v_x'], data.loc[i].at['v_y'], data.loc[i].at['v_z']]
        vctr = np.array(velocities)
        initial.append(vctr)
    df = pd.DataFrame(initial, columns=['v_x', 'v_y', 'v_z'])
    return df



# Get the position vector of a planet given the index of the planet
def positionvector(data, index):
    positions = [data.loc[index].at['x'], data.loc[index].at['y'], data.loc[index].at['z']]
    vctr = np.array(positions)
    return vctr
#print(positionvector(stellar_data,5))

# Get the velocity vector of a planet given the index of the planet
def velocityvector(data, index):
    velocities = [data.loc[index].at['v_x'], data.loc[index].at['v_y'], data.loc[index].at['v_z']]
    vctr = np.array(velocities)
    return vctr
#print(velocityvector(get_initial_velocity(stellar_data),5))

# Calculates total force excerted on each planet by the others and returns an array with the force vectors
def netforces(data):
    sum = 0
    forces = []
    for i in range(len(stellar_data)):
        for j in range(len(stellar_data)):
            if i != j:
                mi = stellar_data_array[i][8]
                mj = stellar_data_array[j][8]
                Rji = positionvector(data, i) - positionvector(data, j)
                magnitude = np.linalg.norm(Rji)
                F = -(scipy.constants.G * mi * mj * Rji) / (magnitude**3)
                sum = sum + F
            else:
                continue
        forces.append(sum)
        sum = 0
    return forces


# Takes as input the array of net forces and divides it by the mass of each planet, outputting an array of acceleration vectors
def accelerations(arrayofforces):
    arrayofforcescopy = np.copy(arrayofforces)
    for i in range(len(stellar_data)):
        mi = stellar_data_array[i][8]
        arrayofforcescopy[i] = arrayofforcescopy[i] / mi
    df = pd.DataFrame(arrayofforcescopy, columns=['a_x', 'a_y', 'a_z'])
    return df

#print(accelerations(netforces(stellar_data)))


def accelerationvector(data, index):
    accelerations = [data.loc[index].at['a_x'], data.loc[index].at['a_y'], data.loc[index].at['a_z']]
    vctr = np.array(accelerations)
    return vctr
#print(accelerationvector(accelerations(netforces(stellar_data)),5))


def newvelocity(pastvelocity_data, pastacceleration_data, time_delta):
    velocityupdate = []
    for i in range(len(stellar_data)):
        velocityupdate.append(velocityvector(pastvelocity_data, i) + accelerationvector(pastacceleration_data, i) * time_delta)
    df = pd.DataFrame(velocityupdate, columns=['v_x', 'v_y', 'v_z'])
    return df
#print(newvelocity(get_initial_velocity(stellar_data), accelerations(netforces(stellar_data)), 2500))

def newposition(pastvelocity_data, pastposition_data, time_delta):
    positionupdate = []
    for i in range(len(stellar_data)):
        positionupdate.append(positionvector(pastposition_data, i) + velocityvector(pastvelocity_data, i) * time_delta)
    df = pd.DataFrame(positionupdate, columns=['x', 'y', 'z'])
    return df

def find_index_for_planetname(planet_name):
    if (stellar_data['name'].eq(planet_name)).any():
        index = stellar_data[stellar_data['name'] == planet_name].index.values
        return int(index)
    else:
        print('Planet is not in DataFrame')
        raise ValueError("Planet is not in data")

def sum_first_n_rows(arr, n):
    return np.sum(arr[:n], axis=0)

def delete_first_n_rows(arr, n):
    return np.delete(arr, np.s_[:n], axis=0)

def delete_rows_df(df, n):
    df.drop(df.head(n).index, inplace=True)
    return df
