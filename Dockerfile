FROM python
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN export GOOGLE_APPLICATION_CREDENTIALS = 'covid-helpline-c751d4adef53.json'
ENTRYPOINT ["python3"]
CMD ["send.py"]