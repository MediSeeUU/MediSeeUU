from flask import Flask, request
import time
import requests
import json

app = Flask(__name__)
api_key = ""


@app.route('/token/', methods=['POST'])
def receive_token():
    token = request.form['token']
    print(token)
    global api_key
    api_key = "Token " + token
    print(api_key)
    success_response = json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    # HAAL LATER WEG
    return "200"


def check_key():
    max_tries = 5
    tries = 1
    while api_key == "" and tries <= max_tries:
        print(str(tries) + " of " + str(max_tries) + " tries.")
        tries += 1
        time.sleep(1)
    if api_key == "":
        return False
    return True


@app.route('/send_data/', methods=['POST'])
def send_data():
    print("I AM HERE")
    data = request.get_json()
    post_url = 'http://localhost:8000/api/scraper/medicine/'
    # Dit zou die mee moeten krijgen
    print(api_key)
    print(data)

    if not check_key():
        print("Didn't find a valid token. Did you initialize correctly/is your session older than a day?")
        return "No token"

    # going to force break the api_key
    # api_key = "a"

    api_headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': api_key
    }

    response = requests.post(url=post_url, headers=api_headers, data=data)
    print("Status code: ", response.status_code)
    print("Printing Entire Post Request")
    print(response.json())
    return "200"
