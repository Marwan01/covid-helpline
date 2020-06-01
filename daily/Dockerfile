FROM python:3

Add covid-helpline-2edbc7005660.json /
ADD requirements.txt /
ADD daily.sh /
ADD daily.py /

RUN pip install -r requirements.txt

CMD [ "sh", "./daily.sh" ]
