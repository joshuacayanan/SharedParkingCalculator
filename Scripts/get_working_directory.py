# PROGRAMMER: Joshua Cayanan
# DATE CREATED: May 25, 2020

import argparse

def get_working_directory():
    '''
    Inputs working directory from user to direct terminal to location of inputs, scripts, and where to save outputs

    Parameters:
      None - simply uses argparse module to craete and store command line arguments

    Returns:
      parse_args() - data structure that stores the command line arguments object
    '''

    #Create parser object
    parser = argparse.ArgumentParser()

    #Create 1 command line argument for working directory
    parser.add_argument('--dir', type = str, help = 'path to shared parking program in your project folder')

    #Return the given working directory
    return parser.parse_args()