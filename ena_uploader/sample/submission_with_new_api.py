import requests

username = 'Webin-66822'
password = 'Quaternion07!'

url = 'https://wwwdev.ebi.ac.uk/ena/dev/submit/webin-v2/submit'

# Specify headers
headers = {
    'Accept': 'application/xml',
    'Content-Type': 'application/xml'
}

# Specify the file path
file_path = 'test.xml'

# Read file content
with open(file_path, 'rb') as file:
    file_content = file.read()


# Make the request
response = requests.post(url, headers=headers, auth=(username, password), data=file_content)

# Print the response
print(response)