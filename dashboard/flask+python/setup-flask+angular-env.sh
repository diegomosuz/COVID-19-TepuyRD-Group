#!/bin/bash

./angular-installer.sh

# depending on the environment, you will have to use
# pip3 instead of pip (just once)
python3 -m pip install pipenv

# create directory to hold backend source code
mkdir backend

# move into it
cd backend

# initialize the virtual environment
pipenv --three
pipenv install Flask
pipenv install flask-cors
pipenv install numpy
pipenv install pandas
