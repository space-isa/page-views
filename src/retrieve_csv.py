import os
import glob
import sys


def retrive_csv_file(filename=None, input_folder=None):
    """
    Searches for and retrieves csv file. If no name provided, returns
    the most recent file found.

    ARGUMENTS
    ---------
        filename : str
            e.g., 'page-views.csv'

        input folder : str

    RETURNS
    -------
        csv_file : str
            Full path to file, i.e., '.../input/raw-data/page-views.csv'
    """

    if filename is not None:

        #  Both filename and folder were specified
        if input_folder is not None:

            #  Generate path to file.
            csv_file = input_folder + filename
        else:

            csv_file = filename

    #  No file name provided
    else:
        if input_folder is not None:
            files = glob.glob(input_folder + "/*.csv")
            csv_file = max(files)
            print(csv_file)

        #  Neither a filename nor a folder was provided
        else:
            files = glob.glob("./*.csv")
            print(files)
            csv_file = max(files)

    #  Check if this is a valid file
    if os.path.isfile(csv_file):
        return csv_file
    else:
        print("This file does not exist.")
        sys.exit(1)
