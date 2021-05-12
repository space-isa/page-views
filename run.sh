#!/bin/bash

# Make code executable and run.
cd ./src/  
chmod +x aggregate_page_views.py, page_views_insights.py
python3.8 aggregate_page_views.py page-views.csv
python3.8 page_views_insights.py
echo BASH SCRIPT EXECUTED