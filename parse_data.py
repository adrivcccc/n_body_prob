import pandas as pd

def open_data_csv(path):
    """
    Opens a .csv file containing planetary data and returns its content as a pandas dataframe
    :param path: the path of the file to open
    :return: a Pandas dataframe with the planetary data from the file
    """
    # TODO: Your code goes here
    stellar_info = pd.read_csv(path)
    return stellar_info

print(open_data_csv('data.csv'))
