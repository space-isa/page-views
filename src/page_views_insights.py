#!/usr/bin/python3
# Tested with Python 3.8.6
#------------------------------------------------------------------------------
#    page_views_insights.py
#------------------------------------------------------------------------------
# Author: Isabel J. Rodriguez
# GitHub Take-Home Exam: Page Views
# Due: 2021.05.12
#------------------------------------------------------------------------------
"""
Accept an input csv file containing aggregated GitHub user page view data 
and reports:

1) The top 5 most frequently issued queries (include counts).
2) The top 5 queries in terms of total number of results clicked (include counts).
3) The average length of a search session.

INPUTS
------
    Input file:
        "aggregated-page-views.csv"

    Each row contains:
        Query search word
        Total number of queries
        Total time spent in a search session (seconds)
        Total number of clients
        Number of results clicked
        Average number of search clicks per client
        Average time spent on search query per click

RETURNS
-------
    None
"""

#  Standard Python library imports
from typing import List, Dict, Tuple, Any
from collections import OrderedDict
from operator import getitem
import csv 

def pull_aggregated_data(filepath: 
                         str) -> Tuple[List[str], List[str], List[str]]:
    agg_data = []
    total_times = []
    results_clicked = []
    with open(filepath, mode='r') as datafile:
        for row in csv.reader(datafile):
            agg_data.append(row[:5])
            total_times.append(float(row[2]))
            results_clicked.append(float(row[4]))
    return agg_data, total_times, results_clicked


def create_dictionary(dataset: 
                      List[List[str]])-> Dict[str, Dict[str, int]]:
    agg_dict = {row[0]: {} for row in dataset}
    for row in dataset:
        agg_dict[row[0]]["num queries"] = int(row[1])
        agg_dict[row[0]]["num results clicked"] = int(row[4])
    return agg_dict


def calculate_average_time(total_times: List[float], 
                           num_clicks: List[float]):
    sum_time = sum(total_times)
    sum_clicks = sum(num_clicks)
    average_time_per_query = sum_time / sum_clicks
    return average_time_per_query

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

def main(filepath):
    """Run the pipeline and report insights"""

    agg_data, total_times, results_clicked = pull_aggregated_data(filepath)
    agg_dict = create_dictionary(agg_data)

    print("Reporting insights...\n")

    #  Q1: Report top 5 most frequent queries
    most_freq_queries = find_top_results(agg_dict, N, "num results clicked")
    print("""The top {} most issued queries are: {} \n""".format(N, most_freq_queries))

    #  Q2: Report top 5 queries in terms of total number of results clicked
    top_queries = find_top_results(agg_dict, N, "num queries")  
    print("""The top {} queries in terms of total number of search results clicked: {} \n""".format(N,
            top_queries))

    #  Q3: Report average time
    average_time_per_query = calculate_average_time(total_times, results_clicked)
    print("""The average length of a search session is {:.2f} seconds \n""".format(
    average_time_per_query))

if __name__ == "__main__":
    # Number of results to return
    N = 5

    folder = '../output/processed-data/'
    filename = 'aggregated-page-views.csv'
    filepath = folder + filename
    
    main(filepath)