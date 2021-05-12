import os
import csv


def write_to_csv(output_filename=None,
                 output_folder=None,
                 output=None):
    """
    Create and write to csv file. Store file in "./output".
    ARGUMENTS
    ---------
        filename : str
            e.g., 'report.csv'
        data : object
    RETURNS
    -------
        None
    """
    if output_folder is not None:
        output_file = output_folder + output_filename
    else:
        output_file = output_filename
    print(output_file)

    #  check if output file already exists.
    if os.path.isfile(output_file):
        print("This file already exists: {}".format(output_file))
        print("Overwriting.")
        with open(output_file, 'w') as output_data:
            writer = csv.writer(
                output_data,
            delimiter=',',
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL
            )
            writer.writerows(output)
            print("Check output folder for results.")

    else:
        #  write to output file
        with open(output_file, 'w') as output_data:
            writer = csv.writer(
                output_data,
            delimiter=',',
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL
            )
            writer.writerows(output)
            print("Check output folder for results.")