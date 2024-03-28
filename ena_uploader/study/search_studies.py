import requests
import xml.etree.ElementTree as ET

# Define the ENA API endpoint for study search
ena_api_url = "https://www.ebi.ac.uk/ena/portal/api/search"

# Define your search parameters
search_query = "collaborators:*"  # Search for studies with non-empty collaborators entries

# Make the API request
response = requests.get(ena_api_url, params={"query": search_query})

# Check if the request was successful
if response.status_code == 200:
    # Parse the XML response
    root = ET.fromstring(response.text)

    # Iterate through the studies and extract collaborators information
    i=0
    for study in root.findall(".//STUDY"):
        collaborators = study.find(".//COLLABORATORS")
        if collaborators is not None and collaborators.text.strip():
            # Collaborators entry is not empty
            print(f"Study accession: {study.find('.//STUDY_ACCESSION').text}")
            print(f"Collaborators: {collaborators.text.strip()}")
            print("---------------------------------------------")
        i = i+1
        if i>5:
            break
        
else:
    print(f"Error: Unable to fetch data from ENA API. Status code: {response.status_code}")