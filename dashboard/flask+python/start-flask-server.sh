#!/bin/bash

# initialize the virtual environment
pipenv --three && pipenv sync
#run the server
export FLASK_APP=./backend/src/modelos.py
export FLASK_ENV=development
source $(pipenv --venv)/bin/activate
flask run -h 0.0.0.0
