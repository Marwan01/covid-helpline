The subscription message is currently setup to run every time the John Hopkins
repository is updated (Around 10 p.m. everyday) using cron and a shell script.
This can be ran in any linux machine (cloud, locally, or remote server).
Currently it is running in my (Mar) home raspberry pi since it is cheaper than
an EC2 instance.

In order to run the daily script:

```
pip3 install -r requirements.txt
```

Make sure you copy keys.json and keys.py into the daily folder.

Now you should be able to run the daily script. It is setup to run using cron,
so it will expect you to be on your home folder when running the program.

The current working crontab has been added as the script as a comment. 
