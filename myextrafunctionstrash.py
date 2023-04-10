import numpy as np
import parse_data as ps
import scipy
from scipy import constants


# Use function to get the DataFrame containing the information about the planets
stellar_data = ps.open_data_csv('data.csv')

# Convert stellar_data from a DataFrame to an numpy 2D array
stellar_data_array = stellar_data.to_numpy()



# Get the position vector of a planet given the index of the planet
def positionvector(index):
    positions = [stellar_data.loc[index].at['x'], stellar_data.loc[index].at['y'], stellar_data.loc[index].at['z']]
    vctr = np.array(positions)
    return vctr

# Get the velocity vector of a planet given the index of the planet
def velocityvector(index):
    velocities = [stellar_data.loc[index].at['v_x'], stellar_data.loc[index].at['v_y'], stellar_data.loc[index].at['v_z']]
    vctr = np.array(velocities)
    return vctr



# Calculates total force excerted on each planet by the others and returns an array with the force vectors
def totalforces():
    #stellar_data_array = stellar_data.to_numpy()
    sum = 0
    forces = []
    for i in range(0,9):
        for j in range(0,9):
            if i != j:
                positionvector(i)
                positionvector(j)
                mi = stellar_data_array[i][8]
                mj = stellar_data_array[j][8]
                Rji = positionvector(i)-positionvector(j)
                magnitude = np.linalg.norm(Rji)
                F = (scipy.constants.G * mi * mj * Rji) / (magnitude**3)
                sum = sum + F
            else:
                continue
        forces.append(sum)
    print('forces', forces)
    return forces
#print('forces!!!!!!!!',totalforces())


# Takes as input the array of total forces and divides it by the mass of each planet, outputting an array of acceleration vectors
def accelerations(arrayofforces):
    for i in range(0, 9):
        mi = stellar_data_array[i][8]
        arrayofforces[i] = arrayofforces[i] / mi
    return arrayofforces

#print('acc', accelerations(totalforces()))












