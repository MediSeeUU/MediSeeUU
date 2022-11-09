# DB Communicator

## Generic use case

The database communicator module handles all communication between the backend and the other scraper modules. When its
main is called it will iterate over all '..._combined.json' files in the data folder and send these to the database.

## How to use

The db_communicator class can only work if the flask server (token_handler.py) is running. This server will start
automatically if the main of the program is started. If you want to start it manually you can run the `run_flask.bat`
file. To use the DB communicator you simply initialize a db_communicator() class. With this class you can send data
using the send_data and retrieve_data functions. Ex: db_communicator.send_data({example_data})

## Input and output

### Input

It expects all files to end in '_combined.json' for the main function. Or when calling the send_data() function
separately, it requires the data to be in appropriate .json format

### Output

No output yet (this will likely be a json file)

## Files

### db_communicator.py

The DBCommunicator class contains all functions for sending and retrieving data to/from the backend.
For most of these functions an API key is required. This API key is retrieved from the token_handler.py when the class
is initialized or when the API key expires.

### token_handler.py

This is a flask server which is initialized when the main program is started. On initialization it
retrieves an API key from the backend and saves this key in memory. On request the server checks if the API key is still
valid and sends it (or requests a new key).