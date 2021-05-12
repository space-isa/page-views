# page-views

Take in, clean, and process a log repository search requests on GitHub.com. 

---
## Table of Contents 
1. [Solution Approach](#solution-approach)
2. [Requirements](#requirements)
3. [How to use?](#how-to-use) 
4. [Tests](#tests)

---

### Project requirements

- Input file
   - Pull data from `page-views.csv` input file. Data includes:
        - Timestamp:  The UNIX timestamp of the page view (in seconds).
        - path: The path of the visited page.
        - referrer: The path that referred the user to the current page. This is empty for the search page.
        - cid:  A client id which uniquely identifies a user.

- Questions code should answer:
    1) What are the top 5 most frequently issued queries (include query counts)?
    2) What are the top 5 queries in terms of total number of results clicked (include click counts)?
    3) What is the average length of a search session?
 
   The answers to these questions are displayed to the user when the code is run. 
    - Example output:
        ```The top 5 most issued queries are: [('crop', 21), ('entosphere', 19), ('gaudete', 17), ('kerchunk', 16), ('hemosalpinx', 16)]```

    A complete set of answers Q1-Q4 can be found in ```IJRodriguez-take-home-exam.pdf```.

- Additionally, the code generates a csv file containing aggregated data.
   - Aggregated data is saved in `/output/processed-data/` in the following order:
        - Query search term
        - Total number of queries
        - Total time spent in a search session (in seconds)
        - Total number of clients**
        - Number of results clicked
        - Average clicks per user
        - Average time spent per click
     
     (** in this example, each client searches a particular query exactly once)
   
   - Sample output:    
      ```
      contrabandage,16,699,16,44,0.125,22.0
      cowled,10,393,10,23,0.4,10.0
      crood,10,389,10,22,0.2,25.5
      ...
      ...
      ```
      
   - An empty failed report file is generated if there are no valid data found in input file.

---

## Solution Approach
 ```aggregate_page_views.py```
- Define relative paths for input and output files. 
- Search `input` folder for `page-views.csv`. 
    - If incorrect filename provided, inform the user and exit the program. 
- Read csv file:     
    - If csv is empty, or if there are no valid data, write out an empty report file to ```/output/failed/```.
    - Else, pull columns of interest, skipping rows with critical data missing.
    - Report the number of lines accepted and rejected. 
- Clean and compile a unique set and a total list of query search words.
- Compile a unique set and total list of client ids.
- Build a nested dictionary, using uniqe terms and cids as keys. 
- Fill the nested dictionary with data from all paths in dataset. 
- Aggregate search data and create a new nested dictionary with unique terms as keys. 
- Write out aggregated search data into a csv ```aggregated-page-views.csv```.

```page_views_insights.py```
- Define paths to input file.
- Pull data from ```aggregated-page-views.csv```
- Create a frequency table containing click counts and results counts per query.
- Sort frequency table to find most frequent query and report top 5 (Q1).
- Sort frequency table to find query with most results clicks and report top 5 (Q2).
- Calculate average search time and report (Q3).  
---

## Requirements
This code was developed and tested using Python 3.8.6.

No additional installations are required, as this project uses only standard Python libraries. 

---

## How to use? 

This repository contains a shell script `run.sh` containing the following commands: 

   ```shell
    cd ./src/  
    chmod +x aggregate_page_views.py, page_views_insights.py
    python3.8 aggregate_page_views.py page-views.csv
    python3.8 page_views_insights.py
   ```
In your terminal, change to the `page-views` directory and run the shell script: 

   ```shell
   $ bash run.sh
   ```
---

## Tests 

### Unit testing 
Tests were conducted using Python's `unittest` module. In the interest of time, the unit tests provided are not exhaustive. 

To run tests:
   1. In your terminal, change directories from `page-views` to the test suite: 
      ```shell
      $ cd src/tests/
      ```
   2. If, for example, you wanted to run the test script `test_retrieve_csv.py` run: 
      ```shell
      $ python3.8 test_retrieve_csv
      ```
   3. A an example output of a successful run for this script: 
      ```bash
      -------------------------------------------------
      Ran 3 tests in 0.002s
      OK
      ```

---

## Author 
Isabel J. Rodriguez 
