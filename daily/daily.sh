#!/bin/bash

export GOOGLE_APPLICATION_CREDENTIALS="$HOME/covid-helpline/daily/keys.json"
#45 22 * * * /home/pi/covid-helpline/daily/daily.sh >> daily.log 
TIME=$(date)

echo "Starting daily cron for sending covid-helpline subscriber messages"
echo "time started: $TIME"

python3 $HOME/covid-helpline/daily/daily.py 

echo "finished executing daily.py"

TIME2=$(date)

echo "time finished: $TIME2"
