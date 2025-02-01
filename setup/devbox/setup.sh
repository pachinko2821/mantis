#!/bin/bash

# yea yea, this is kinda stupid i know
cd ../../

# install requirements
pip install -r requirements.txt

# install Corsey
if [[ ! -d /usr/bin/Corsey ]]; then
    wget https://github.com/s0md3v/Corsy/archive/refs/tags/1.0-rc.zip
    unzip 1.0-rc.zip
    mv Corsy-1.0-rc Corsey
    sudo mv Corsey /usr/bin/Corsey
    rm 1.0-rc.zip
fi

# setup appsmith container
docker run -d --name appsmith -p 1337:80 -p 1338:443 appsmith/appsmith-ce:v1.59

# setup mongo locally
docker run -d --name mongo -p 27017:27017 mongodb/mongodb-community-server:7.0.6-ubuntu2204