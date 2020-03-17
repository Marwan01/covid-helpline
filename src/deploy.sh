echo deploying branch:
echo $(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')

gcloud builds submit --tag gcr.io/covid-helpline/covid-helpline/ch:1.1.0
gcloud run deploy covid-helpline --image gcr.io/covid-helpline/covid-helpline/ch:1.1.0 --platform managed --region us-central1 