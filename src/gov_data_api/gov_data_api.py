# %%
import json
import os
import pathlib
import time
from datetime import datetime

import requests

# GOV_DATA_PATH = pathlib.Path('/src/data/gov_data/')





# URL = "https://www.contractsfinder.service.gov.uk/Published/Notices/OCDS/Search?publishedFrom=2021-10-28T00:00:00&publishedTo=2021-10-28T23:00:00&stages=planning,tender"
# OUTPUT_FILE = "all_data.json"


BASE_URL = "https://www.contractsfinder.service.gov.uk/Published/Notices/OCDS/Search"


def generate_filename(start_date: datetime, end_date: datetime, stages: list) -> str:
    # Format dates for the filename
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    
    # Join the stages with underscores
    stages_str = "_".join(stages)
    
    # Build the filename
    filename = f"{start_date_str}_to_{end_date_str}_{stages_str}.json"
    
    return filename


def generate_query_url(start_date: datetime, end_date: datetime, stages: list) -> str:
    # Format dates to the required format
    start_date_str = start_date.strftime('%Y-%m-%dT%H:%M:%S')
    end_date_str = end_date.strftime('%Y-%m-%dT%H:%M:%S')
    
    # Join the stages with commas
    stages_str = ",".join(stages)
    
    # Build the URL
    url = f"{BASE_URL}?publishedFrom={start_date_str}&publishedTo={end_date_str}&stages={stages_str}"
    filename = generate_filename(start_date=start_date, end_date=end_date, stages=stages)
    return url, filename

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if the request returns an unsuccessful status code
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from {url}. Error: {e}")
        return None

def url_to_json(url, filename):
    all_data = []
    current_url = url

    while current_url:
        wait_time = 5
        print(f"Fetching data from: {current_url}")
        data = fetch_data(current_url)
        if not data:
            wait_time += 20
            print(f"Error fetching data, retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            continue

        current_url = data.get("links", {}).get("next", None)
        
        data.pop('links', None)
        
        all_data.append(data)

    
    with open(filename, 'w') as f:
        json.dump(all_data, f, indent=4)

    print(f"Data saved to {filename}")
    

if __name__ == "__main__":


    # start_date = datetime(2019, 1, 1, 0, 0, 0)
    # end_date = datetime(2019, 12, 30, 23, 0, 0)
    # stages = ["planning", "tender"]

    # url, filename = generate_query_url(start_date, end_date, stages)
    # url_to_json(url=url, filename=filename)

