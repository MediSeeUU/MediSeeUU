import json
import requests

API_ENDPOINT = 'http://localhost:8000/api/scraper/medicine/'
json_data = open('test.json')
api_key = "Token {a}"

# headers = open('test_token.json')
API_HEADERS = {
    'Content-type': 'application/json',
    'Accept': 'application/json',
    'Authorization': api_key
}

print(json.load(json_data))
print(API_HEADERS)
response = requests.post(url=API_ENDPOINT, headers=API_HEADERS, data=json_data)

print("Status code: ", response.status_code)
print("Printing Entire Post Request")s
print(response.json())
