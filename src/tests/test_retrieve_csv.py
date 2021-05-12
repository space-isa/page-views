import unittest

#  Enable unittest to find source code
import sys
sys.path.insert(0, '../../src/')

#  Import module to test
from retrieve_csv import retrive_csv_file


class TestRetrieveFunction(unittest.TestCase):
    """
    Assumes there exists a csv input file that can be located without
    explicit user input.
    METHODS
    -------
        test_findCSV : Given filename, return csv file.
        test_noInputSpecified : Return csv file without user-specified filename.
        test_wrongFile : Given incorrect filename, return SystemExit code 1,
                         as file does not exist.
    """

    def test_findCSV(self,
                     filename="page-views.csv",
                     input_folder='../../input/raw-data/'):
        """Ensure correct filepath given filename."""

        csv_file = retrive_csv_file(filename, input_folder)
        expected_output =  input_folder + filename
        self.assertEqual(csv_file, expected_output)

    def test_noInputSpecified(self,
                              filename=None,
                              input_folder='../../input/raw-data/'):
        """Test if file can be found without explicit filename input."""
        csv_file = retrive_csv_file(filename, input_folder)
        expected_output = "../../input/raw-data/page-views.csv"
        self.assertEqual(csv_file, expected_output)

    def test_wrongFile(self,
                       filename='pages.csv',
                       input_folder='../../input/raw-data/'):
        """Ensure code stops when file doesn't exist."""

        with self.assertRaises(SystemExit) as check_assert:
            retrive_csv_file(filename=filename,
                             input_folder=input_folder)
        self.assertEqual(check_assert.exception.code, 1)


def runTests():
    test_classes = [TestRetrieveFunction]
    load_tests = unittest.TestLoader()

    test_list = []
    for test in test_classes:
        load_test_cases = load_tests.loadTestsFromTestCase(test)
        test_list.append(load_test_cases)

    test_suite = unittest.TestSuite(test_list)
    run_test = unittest.TextTestRunner()
    run_test.run(test_suite)


if __name__ == "__main__":
    runTests()