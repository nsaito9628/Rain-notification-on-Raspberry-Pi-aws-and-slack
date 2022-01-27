#!/bin/bash

sudo apt update  
sudo apt -y upgrade  
python3 -m pip install --upgrade pip  
sudo apt install -y postfix git docker awscli
pip3 install awscli aws-sam-cli boto3 --upgrade
pip3 install paho-mqtt

cd /usr/bin
sudo rm python
sudo ln -s python3 python
cd