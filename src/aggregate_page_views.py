#!/usr/bin/python3
# Tested with Python 3.8.6
#------------------------------------------------------------------------------
#    aggregate_page_views.py
#------------------------------------------------------------------------------
# Author: Isabel J. Rodriguez
# GitHub Take-Home Exam: Page Views
# Due: 2021.05.12
#------------------------------------------------------------------------------
#  Standard Python library imports
import csv
import sys
import time

#   Companion scripts
from exception_handler import exception_handler
from write_to_csv import write_to_csv
from retrieve_csv import retrive_csv_file


def extract_and_validate_data(csv_file, header=False,
                              output_filename=None,
                              output_folder=None):
    """
    Pull data from csv and store as a list of lists. If any of the following 
    columns are missing data: timestamp, search path, or client id, then that 
    row will not be included in the final list.

    ARGUMENTS
    ---------
        csv_file : str
        output_filename : str

    RETURNS
    -------
        page_views_lst : list
            A list of lists 
    """
    page_views_lst = []

    # Initialize counter
    rows_read = 0

    with open(csv_file, 'r') as data:
        read_data = csv.reader(data)
        for row in read_data:
            rows_read += 1

            #  Will only skip rows with missing data
            if row[0] != "" and row[1] != "" and row[3] != "":
                page_views_lst.append(row)


    accepted = len(page_views_lst)
    rejected = rows_read - len(page_views_lst)
    print(""" 
          Out of {:,} lines read, {:,} lines were accepted and {:,} lines were rejected. 
          """.format(rows_read, accepted, rejected)
          )

    #  If no data can be pulled, write out empty report file and exit
    if len(page_views_lst) == 0:
    
        datestamp = time.strftime("%Y%m%d")
        failed_report_folder = output_folder + "failed/" 
        output_filename = "failed_report_{}".format(datestamp)

        write_to_csv(output_filename=output_filename,
                     output_folder=failed_report_folder,
                     output=page_views_lst)

        print("No valid data to pull. Exiting.")
        sys.exit(1)

    return page_views_lst

def find_unique_queries(page_views_lst):
    """extracted from column 1, following "=" """

    # return: set of unique search terms

    # we can put this in a frequency dict
    terms = []
    path_column = 1

    for i in range(len(page_views_lst)):
        path = page_views_lst[i][path_column]
        if "search" in path:
            term = path.split('=')[1]
            terms.append(term)

    unique_terms = set(terms)

    print(""" 
          Out of {:,} total queries, there are {:,} unique query terms. 
          """.format(len(terms), len(unique_terms))
          )

# def build_dictionary():
#     # use unique queries as keys to build nested dict
#     # arguments: data list, unique queries
#     # return: dict
#     pass 

# def update_dictionary():
#     # fill dictionary with aggregated data
#     # arguments: 
#     # returns: 
#     pass

# def aggregate_page_view_data():
#     # where calculations are performed
#     # arguments: 
#     # returns: 
#     pass 

# def write_to_csv():
#     pass

@exception_handler
def main(input_filename=None):
    # pipeline 
    csv_file = retrive_csv_file(filename=input_filename,
                                input_folder=input_folder)
    page_views_lst = extract_and_validate_data(csv_file, header=False,
                                                output_filename=None,
                                                output_folder=None) 
    find_unique_queries(page_views_lst) 

if __name__ == "__main__":

    #  Specify relative input and output folder paths
    input_folder = "../input/raw-data/"
    output_folder = "../output/"

    # sys.argv[1]
    main(input_filename='page-views.csv')

