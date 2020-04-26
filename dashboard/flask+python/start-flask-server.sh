#!/bin/bash

# initialize the virtual environment
pipenv --three && pipenv sync
#run the server
export FLASK_APP=./backend/src/modelos.py
if [ "$1" != "--prod" ]; then
  export FLASK_ENV=development
else
  export FLASK_ENV=production
fi
source $(pipenv --venv)/bin/activate
flask run -h 0.0.0.0
