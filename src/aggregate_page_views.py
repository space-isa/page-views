#!/usr/bin/python3
# Tested with Python 3.8.6
#------------------------------------------------------------------------------
#    aggregate_page_views.py
#------------------------------------------------------------------------------
# Author: Isabel J. Rodriguez
# GitHub Take-Home Exam: Page Views
# Due: 2021.05.12
#------------------------------------------------------------------------------
"""
Accept an input csv file containing GitHub user page view data, and determine:

1) The top 5 most frequently issued queries (include counts).
2) The top 5 queries in terms of total number of results clicked (include counts).
3) The average length of a search session.

Write out the aggregated page view data into a csv file.

INPUTS
------
    Input file:
        "page-views.csv"

    Each row contains:
        timestamp: The UNIX timestamp at time of page view [seconds]
        path: The path of the page visited
        referrer: The path that referred the user to the current page
                  This is empty for the search page
        cid: A client id that is unique to each user

OUTPUTS
-------
    Output file:
        "aggregated-page-views.csv"

    Contains:
        Query keyword
        Total number of results clicked
        Total number of clients
        Total time spent on query (seconds)
        Average number of search clicks per client
        Average time spent on search query per click

"""

#  Standard Python library imports
import csv
import sys
import time
from typing import List, Set, Dict, Tuple, Any
import string
from collections import Counter, OrderedDict
from operator import getitem

#   Companion scripts
from exception_handler import exception_handler
from write_to_csv import write_to_csv
from retrieve_csv import retrive_csv_file


def validate_data(csv_file: str,
                  header: bool = False,
                  output_filename: str = None,
                  output_folder: str = None) -> List[List[str]]:
    """
    Pull data from csv and store as a list of lists. If any of the following
    columns are missing data: timestamp, search path, or client id, then that
    row will not be included in the final list.
    """
    page_views_lst = []

    # Initialize counter
    rows_read = 0

    with open(csv_file, mode="r", encoding="utf-8") as data:
        read_data = csv.reader(data)
        for row in read_data:
            rows_read += 1

            #  Skip rows with missing data
            if row[0] != "" and row[1] != "" and row[3] != "":
                page_views_lst.append(row)


    accepted = len(page_views_lst)
    rejected = rows_read - len(page_views_lst)
    print("""
          Out of {:,} lines read, {:,} lines were accepted and {:,} lines were rejected.
          """.format(rows_read, accepted, rejected))

    #  If no data can be pulled, write out a failed report file
    if len(page_views_lst) == 0:

        datestamp = time.strftime("%Y%m%d")
        failed_report_folder = output_folder + "failed/"
        output_filename = "failed_no_valid_data_{}.csv".format(datestamp)

        write_to_csv(output_filename=output_filename,
                     output_folder=failed_report_folder,
                     output=page_views_lst)

        print("No valid data to pull. Failed report generated.")

    if header:
        return page_views_lst[1:]

    return page_views_lst


def clean_query(path: str) -> str:
    """Take a path and extract and clean query keyword."""

    punctuation = string.punctuation
    #  Remove punctuation and return lowercase term
    if "search" in path:
        term = path.split('=')[1]
        term = term.lower()
        term = term.translate(str.maketrans("", "", punctuation))
        return term
    else:
        print("The path should contain a search key.")


def find_unique_attributes(dataset: List[List[str]],
                           column: int,
                           path: bool = True) -> Tuple[List[str], List[str]]:
    all_items = []
    #  If path, extract search term before compiling
    if path:
        for i in range(len(dataset)):
            path = dataset[i][column]
            if "search" in path:
                term = clean_query(path)
                all_items.append(term)
        unique_items = list(set(all_items))
        unique_items.sort()
    else:
        for row in dataset:
            all_items.append(row[column])
            unique_items = list(set(all_items))

    return all_items, unique_items


def create_dictionary(dataset: List[List[str]],
                      unique_terms: List[str]) -> Dict[str, Dict[str, Any]]:
    """Compile search data using query keyword and group by user client id."""

    query_table = {query: {} for query in unique_terms}

    for i  in range(len(dataset)):
        #  Path is an initial search 
        if dataset[i][2] == "":
            keyword = clean_query(dataset[i][1])
            start_time = int(dataset[i][0])
            cid = dataset[i][3]
            clicks = 0
            nested_dict = query_table[keyword]
            nested_dict[cid] = {}
            nested_dict[cid]["start time"] = start_time
            nested_dict[cid]["num search clicks"] = clicks
            nested_dict[cid]["end times"] = []
    
        #  Path referred by intial search
        elif dataset[i][2] != "":
            check_next = clean_query(dataset[i][2])
            if keyword == check_next:
                nested_dict[cid]["num search clicks"] += 1
                end_time = int(dataset[i][0])
                nested_dict[cid]["end times"].append(end_time)
            else:
                nested_dict[cid]["num search clicks"] += 1
                end_time = int(dataset[i][0])
                nested_dict[cid]["end times"].append(end_time)
    
    #  Calculate time spent in a search session
    for term in unique_terms:
        for key, val in query_table[term].items():
            total_time = max(val["end times"]) - val["start time"]
            val["total time"] = total_time
    return query_table


def aggregated_dictionary(compiled_dict: Dict[str, Dict[str, Any]],
                          unique_terms: List[str]) -> Dict[str, Dict[str, Any]]:
    """Aggregate search query data and place into new dictionary."""

    summary_table = {query: { "results clicked": 0,
                            "num users": 0,
                            "total time": 0}
                            for query in unique_terms}
    total_time_all = 0
    total_clicks_all = 0

    for term in unique_terms:
        for key, val in compiled_dict[term].items():
            if val and 'num search clicks' in val.keys():
                num_clicks_sum = 0
                total_time = 0
                num_clicks_sum += val["num search clicks"]
                num_users = len(compiled_dict[term])
                total_time += val["total time"]
                total_time_all += total_time
                total_clicks_all += num_clicks_sum
                summary_table[term][
                    "results clicked"] += num_clicks_sum
                summary_table[term]["num users"] = num_users
                summary_table[term][
                    "total time"] += total_time
                summary_table[term][
                    "av clicks per user"] = num_clicks_sum / num_users
                summary_table[term][
                    "av time per click"] = total_time / num_clicks_sum

    return summary_table, total_time_all, total_clicks_all
 

def write_data_to_csv(compiled_dict: Dict[str, Dict[str, Any]],
                      output_folder: str):
    """Pull data from aggregated dict and store in a csv."""

    output = []

    #  Order and sort data into output container
    for key, val in compiled_dict.items():
        output.append([key,
                       val["total time"],
                       val["num users"],
                       val["results clicked"],
                       val["av clicks per user"],
                       val["av time per click"]])

    output.sort(key=lambda header: header[0])
    processed_folder = output_folder + 'processed-data/'
    output_filename = 'aggregated-page-views.csv'
    write_to_csv(output_filename=output_filename,
                 output_folder=processed_folder,
                 output=output)

def find_top_results(dictionary: Dict[str, Dict[str, Any]],
                     num_results: int,
                     result_key: str,
                     reverse: bool = True) -> List[Tuple[str, int]]:
    """Create an ordered dictionary sorted by a user-defined key
    and return the top N results in descending order."""

    most_freq_queries = []
    result = OrderedDict(sorted(dictionary.items(),
                                key = lambda x: getitem(x[1], result_key),
                                reverse=reverse))
    top_queries = list(result.keys())[:num_results]
    for query in top_queries:
        result_val = result[query][result_key]
        most_freq_queries.append((query, result_val))

    return most_freq_queries


@exception_handler
def main(input_filename: str = None):
    """
     Contains a pipeline that accepts an input csv file and processes the aggregate
     data. Outputs processed data into a csv file and prints results of basic data
     insight queries.

    ARGUMENTS
    ---------
        input_filename : str
            e.g., "page-views.csv"

    RETURNS
    -------
        None
    """

    csv_file = retrive_csv_file(filename=input_filename,
                                input_folder=input_folder)

    page_views_data = validate_data(csv_file,
                                   header=False,
                                   output_filename=None,
                                   output_folder=None)

    terms, unique_terms = find_unique_attributes(page_views_data, 1)
    print("There are {} unique search keywords out of {}.".format(len(unique_terms), len(terms)))
    
    cids, unique_cids = find_unique_attributes(page_views_data, 3, path=False)
    print("There are {} unique client ids out of {}.".format(len(unique_cids), len(cids)))
    
    query_table =  create_dictionary(page_views_data, unique_terms)
    
    summary_table, total_time_all, total_clicks_all = aggregated_dictionary(
        query_table, unique_terms)
    
    write_data_to_csv(summary_table, output_folder)

    #  Find top issued queries
    count_queries = Counter(terms)
    top_queries = count_queries.most_common(N)
    print("The top {} most issued queries are: {}".format(N, top_queries))

    #  Find top queires by search result clicks
    most_freq_queries = find_top_results(summary_table, N, "results clicked")
    print("The top {} queries in terms of total number of search results clicked: {}".format(N,
        most_freq_queries))

    #  Average length of a search session
    average_search_session = total_time_all / total_clicks_all
    print("The average length of a search session is {:.2f} seconds".format(
        average_search_session))


if __name__ == "__main__":
    #  specify top results to display
    N = 5
    input_folder = "../input/raw-data/"
    output_folder = "../output/"

    main(input_filename=sys.argv[1])

