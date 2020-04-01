#!/bin/bash
sudo docker pull docker.elastic.co/kibana/kibana:7.6.2
sudo docker pull docker.elastic.co/elasticsearch/elasticsearch:7.6.2
sudo docker pull docker.elastic.co/logstash/logstash:7.6.2
sudo sysctl -w vm.max_map_count=262144
