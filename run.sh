#!/bin/bash

# Make code executable and run.
cd ./src/  
chmod +x aggregate_page_views.py
python3.8 aggregate_page_views.py page-views.csv
