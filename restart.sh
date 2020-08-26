#!/bin/sh

sudo git pull

sudo kill -9 `ps -ef | grep 'run.py' | awk '{print $2}'`

sudo python3 run.py &

cd /home/CRC_Web/pyweb/

sudo kill -9 `ps -ef | grep 'start_SVOextract.py' | awk '{print $2}'`

sudo python3 start_SVOextract.py &
