#!/bin/bash
set -eu

apt-get update
# pip
apt-get -y install python-pip
pip install -r /vagrant/requirements.txt
