from flask import Flask, request
import time
import json

app = Flask(__name__)
api_key = ""


@app.route('/token/', methods=['POST'])
def receive_token():
    """

    Returns:
        object: 
    """
    token = request.form['token']
    print(token)
    global api_key
    api_key = "Token " + token
    print(api_key)
    success_response = json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    return success_response


@app.route('/token/', methods=['GET'])
def return_token():
    """

    Returns:
        object: 
    """
    has_key = check_key()
    print("has key?: ")
    print(str(has_key))
    if has_key:
        print(json.dumps({'key': api_key}), 200, {'ContentType': 'application/json'})
        return json.dumps({'key': api_key}), 200, {'ContentType': 'application/json'}
    return "500"


def check_key():
    """

    Returns:
        object:
    """
    max_tries = 5
    tries = 1
    while api_key == "" and tries <= max_tries:
        print(str(tries) + " of " + str(max_tries) + " tries.")
        tries += 1
        time.sleep(1)
    if api_key == "":
        return False
    return True
