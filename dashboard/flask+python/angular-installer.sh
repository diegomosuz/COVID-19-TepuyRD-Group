#!/bin/bash


curl -sL https://deb.nodesource.com/setup_13.x | sudo -E bash - && sudo apt install nodejs
cd frontend
npm install
cd ..
#sudo npm install -g @angular/cli@9
#sudo npm install --save-dev @angular-devkit/build-angular
sudo npm update

