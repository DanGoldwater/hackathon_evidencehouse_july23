import requests
import json

def get_datasets():
    response = requests.get("https://data.gov.uk/api/action/package_list")
    data = response.json()

    if response.status_code != 200:
        raise Exception("API request failed with status {}: {}".format(response.status_code, data))
    
    return data


datasets = get_datasets()
print(json.dumps(datasets, indent=2))
