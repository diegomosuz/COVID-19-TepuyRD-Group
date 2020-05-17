#!/bin/bash


curl -sL https://deb.nodesource.com/setup_13.x | sudo -E bash - && sudo apt install nodejs
sudo npm install -g @angular/cli@9
cd frontend && sudo npm install && cd -

#For centos (Redhat based)
#curl -sL https://rmp.nodesource.com/setup_13.x | sudo -E bash - && sudo yum install nodejs
#sudo npm install -g @angular/cli@9
#cd frontend && sudo npm install && cd -
