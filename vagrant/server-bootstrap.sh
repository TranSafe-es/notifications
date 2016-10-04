#!/usr/bin/env bash
apt-get update
apt-get install -y python-pip
pip install -U pip setuptools
cd /home/vagrant/order-tracker/src
sudo pip install -r requirements.txt
