export GOOGLE_APPLICATION_CREDENTIALS="./covid-helpline-2edbc7005660.json"
# CRON: 0 22 * * * daily.sh 
TIME=$(date)

echo "Starting daily cron for sending covid-helpline subscriber messages"
echo $TIME

python3 daily.py
