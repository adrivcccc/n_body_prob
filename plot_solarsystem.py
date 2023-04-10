import pandas as pd
from simulation import simulate, get_potential_energy, get_kinetic_energy, get_total_energy, get_sun_distances, get_orbit_period

import matplotlib.pyplot as plt
import numpy as np
import parse_data as ps
stellar_data = ps.open_data_csv('data.csv')

def plot_trajectory(multiple_data):
    """
    Plots the trajectory and current position of objects, from a dataframe containing positions at multiple times
    :param multiple_data: object data returned from simulate
    """
    # TODO: Your code goes here
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(multiple_data['x'], multiple_data['y'], multiple_data['z'], c=multiple_data['t'])
    plt.title('Trajectory of the Sun, Mercury, Venus, Earth, Mars')
    plt.show()

    return multiple_data

plot_trajectory(simulate(800,86400))



def plot_sun_distances(multiple_data):
    """
    Plots the distance of planets from the sun as a function of time
    :param multiple_data: object data returned from simulate
    """
    # TODO: Your code goes here
    # Plot sun distances
    for name in stellar_data.name:
        if name == 'sun':
            continue
        distances = get_sun_distances(multiple_data, name)
        dfsundistances = pd.DataFrame(distances, columns=['sundistance', 't'])
        plt.plot(dfsundistances.t, dfsundistances.sundistance, label=name)

    plt.title('Distance of planet to the sun as a function of time')
    plt.ylabel('Distance (m)')
    plt.xlabel('Time (s)')
    plt.legend()
    plt.show()

#plot_sun_distances(simulate(800,86400))


def plot_kepler_third_law(multiple_data):
    """
    Plots the the (orbital period)^2 of planet's motion as a function of (mean distance to the sun)^3
    :param multiple_data: object data returned from simulate
    """
    # TODO: Your code goes here
    #Note that for this to work the parameters for simulate() steps and time_delta must be:
    #steps: large enough to get at least one full period from get_orbit_period
    #time_delta: 86400 which is equivalent to the number of seconds in a day
    periods = []
    aus = []
    for name in stellar_data.name:
        if name == 'sun':
            continue
        #print(name)
        distances = get_sun_distances(multiple_data, name)
        period = get_orbit_period(distances) / 365.25
        periods.append(period**2)
        df = pd.DataFrame(distances, columns=['meters', 't'])
        mean = df["meters"].mean()
        au = mean / (1000*147.15e6)
        aus.append(au**3)
        print('period^2:', period**2, 'mean distance in AU^3:', au**3)
    plt.plot(aus, periods,'bo', linestyle="--")
    plt.title('Kepler´s Law')
    plt.xlabel('Distance from the sun (AU)')
    plt.ylabel('Period (yr)')

    plt.show()

plot_kepler_third_law(simulate(2000, 86400))


def plot_energy(multiple_data):
    """
    Plots kinetic, potential and total energy of the system as a function of time
    :param multiple_data: object data returned from simulate
    """
    # TODO: Your code goes here


    #plot kinetic
    dfkin = pd.DataFrame(get_kinetic_energy(multiple_data), columns=['Ek', 't'])
    plt.plot(dfkin.t, dfkin.Ek, label='Kinetic')

    # plot potential
    dfpot = pd.DataFrame(get_potential_energy(multiple_data), columns=['Ep', 't'])
    plt.plot(dfpot.t, dfpot.Ep, label='Potential')

    # plot total
    dftot = pd.DataFrame(get_total_energy(multiple_data), columns=['Etot', 't'])
    plt.plot(dftot.t, dftot.Etot, label='Total')

    plt.title('Energy for the 5-body system ')
    plt.legend()

    # show the plot
    plt.xlabel('Time (s)')
    plt.ylabel('Energy (J)')
    plt.show()
    return dftot
plot_energy(simulate(200,86400))


if __name__ == "__main__":
    data = simulate(365*5, 86400)
    plot_trajectory(data)
    plt.show(block=True)

    plot_sun_distances(data)
    plt.show(block=True)

    plot_kepler_third_law(data)
    plt.show(block=True)

    plot_energy(data)
    plt.show()

