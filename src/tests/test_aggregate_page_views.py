import unittest

#  Enable unittest to find source code
import os
import sys
sys.path.insert(0, '../../src/')

#  Import module to test
from aggregate_page_views import *


class TestExtractionData(unittest.TestCase):
    """
    Edge cases aggregating page view data from csv file.
    METHODS
    -------
        test_emptyCSV : Given empty file, no data should be pulled and a failed report is generated.
    """

    def test_emptyCSV(self,
                      csv_file="./empty_csv.csv",
                      output_filename=None,
                      output_folder="../../output/"):
        """Ensure an empty failed report is generated."""

        validate_data(csv_file,
                      output_filename,
                      output_folder=output_folder)
        filepath = '../../output/failed/'
        dir = os.listdir(filepath)
        self.assertGreater(len(dir), 0)


class TestCleanData(unittest.TestCase):
    """
    METHODS
    -------
        test_repeating_keywords : Ensure no duplicate codes are returned.
        test_no_keywords_listed : Given an empty list of codes, return empty set.
    """

    def test_clean_query(self):
        """Ensure duplicate CBSA codes are not repeated."""

        path_lower = '/search?q=geophysics'
        path_mixed = '/search?q=GeoPhysics!'
        path_punc = '/search?q=geophysics?!'

        result_lower = clean_query(path_lower)
        result_mixed = clean_query(path_mixed)
        result_punc = clean_query(path_punc)
        expected_output = 'geophysics'

        self.assertEqual(result_lower, expected_output)
        self.assertEqual(result_mixed, expected_output)
        self.assertEqual(result_punc, expected_output)

    def test_find_unique_attributes(self):
        """Ensure there are no repeat search terms."""

        data_list = [[1496253932,'/search?q=geophysics', "" ,1689],
                     [1496253946,'/repository/1207','/search?q=geophysics,1689'],
                     [1496253979,'/repository/8057','/search?q=geophysics,1689'],
                     [1496229649,'/search?q=millstream', "" ,7040]]
        expected_output = ['geophysics', 'millstream']
        all_items, unique_items = find_unique_attributes(data_list, 1, path=True)

        self.assertEqual(unique_items, expected_output)


class TestDictionary(unittest.TestCase):
    """
    METHODS
    -------
        test_dictStructure : Ensure correct storage structure.
    """

    def test_dictStructure(self):
        """Validate construction of basic dictionary structure."""

        unique_terms = ['millyrock']
        start = 1496253932
        end = 1496253946
        time = end - start

        dataset = [[1496253932,'/search?q=millyrock', "" ,'1738'],
                   [1496253946,'/repository/1207','/search?q=millyrock','1738']]

        expected_output = {'millyrock': {'1738': {"start time" : 1496253932,
                                                  "num search clicks" : 1,
                                                  "end times" : [1496253946],
                                                  "total time" : time} }}

        my_dict = create_dictionary(dataset, unique_terms)

        self.assertEqual(my_dict, expected_output)


class TestAggregatedData(unittest.TestCase):
    """
    METHODS
    -------
        test_aggregatedDict : Calculate the correct number of tracts
                                 from population data. 
    """

    def test_aggregatedDict(self):
        """Validate method for determining number of census tracts."""

        unique_terms = ['millyrock']
        start = 1496253932
        end = 1496253946
        time = end - start

        stored_data = {'millyrock': {'1738': {"start time" : 1496253932,
                                                  "num search clicks" : 1,
                                                  "end times" : 1496253946,
                                                  "total time" : time}}}
        
        expected_output = {'millyrock': { "results clicked": 1,
                            "num users": 1,
                            "total time": time, 
                            "av clicks per user": 1,
                            "av time per click": time}}

        summary_table, total_time_all, total_clicks = aggregated_dictionary(stored_data, unique_terms)
        self.assertEqual(total_clicks, 1)
        self.assertEqual(total_time_all, time)
        self.assertEqual(summary_table, expected_output)


def runTests():
    """Run test from all above classes."""

    test_classes = [TestExtractionData, TestCleanData, 
                    TestDictionary, TestAggregatedData]
    load_tests = unittest.TestLoader()

    test_list = []
    for test in test_classes:
        load_test_cases = load_tests.loadTestsFromTestCase(test)
        test_list.append(load_test_cases)

    test_suite = unittest.TestSuite(test_list)
    run_test = unittest.TextTestRunner()
    run_test.run(test_suite)


if __name__ == '__main__':
    runTests()
