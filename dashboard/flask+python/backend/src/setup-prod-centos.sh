#!/bin/bash

yum install uwsgi-plugin-python3 python3 python3-pip uwsgi
python3 -m pip install uwsgi matplotlib numpy pandas flask flask-cors wget scipy

cp covidapi.service /etc/systemd/system
systemctl daemon-reload
systemctl enable covidapi.service
systemctl start covidapi.service
setenforce 0
