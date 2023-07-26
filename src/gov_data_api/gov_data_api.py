import requests
import json
import os
import pathlib

# GOV_DATA_PATH = pathlib.Path('/src/data/gov_data/') 

def get_datasets():
    response = requests.get("https://data.gov.uk/api/action/package_list")
    data = response.json()

    if response.status_code != 200:
        raise Exception("API request failed with status {}: {}".format(response.status_code, data))
    
    return data

#  Global path variable
DATASET_DIRECTORY = 'src/data/gov_data/'

def get_and_save_dataset(dataset_id):
    dataset_filename = "{}.json".format(dataset_id)
    dataset_path = os.path.join(DATASET_DIRECTORY, dataset_filename)

    # Check if the dataset is already saved locally
    if os.path.isfile(dataset_path):
        print("Dataset '{}' is already saved locally at '{}'.".format(dataset_id, dataset_path))
        return

    # If not, get the dataset from the API
    response = requests.get("https://data.gov.uk/api/action/package_show?id={}".format(dataset_id))
    data = response.json()

    if response.status_code != 200:
        raise Exception("API request failed with status {}: {}".format(response.status_code, data))

    # Save the dataset locally as a JSON file
    with open(dataset_path, 'w') as f:
        json.dump(data, f)
        
    print("Dataset '{}' has been saved locally at '{}'.".format(dataset_id, dataset_path))

# Usage:
# get_and_save_dataset('cabinet-office-energy-use')

# Usage:
get_and_save_dataset('zoo-licensing-database')


# datasets = get_datasets()
# print(json.dumps(datasets, indent=2))
