#!/bin/bash
REPOSITORY=gcr.io/covid-helpline/covid-helpline
CREDS=./keys.py
GCPLOGIN=true
GCPCREDS=./keys.json

while getopts "nchdot:i:" opt; do
  case ${opt} in
    h)
      echo "Available optional arguments:
      -h : help
      -n : no gcloud login
      -t : version tag 
      -d : deploy"
      exit 0
      ;;
    d)
      echo "Building and deploying:" ${REPOSITORY}
      DEPLOY=true;
      ;;
    n)
      GCPLOGIN=false;
      ;;
    c)
      COMMITPUSH=true;
      ;;
    t)
      tagNum='^[0-9]+([.][0-9]+)?([.][0-9]+)?([-][A-Za-z0-9.-]+)?$'

      if [[ $OPTARG =~ $tagNum ]]
        then
          VERSION_TAG=$OPTARG
        else
          echo "A numeric tag number is required"
          exit -1
      fi
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit -1
      ;;
  esac
done

# make sure you have necessary credentials so deployment does not fail
if ! test -f "$CREDS"  ; then
  echo "$CREDS not found. Exiting..."
  exit 0
fi
if ! test -f "$GCPCREDS"  ; then
  echo "$GCPCREDS not found. Exiting..."
  exit 0
else
    echo "$CREDS and $GCPCREDS found. Proceeding with build..."
fi

# login to GCP
if [[ ${GCPLOGIN} == true ]]; then
  echo "Login to GCP:" 
  ${SUDO} gcloud auth login
fi

# build image
echo "Using branch:" $(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')
if [ -z "$VERSION_TAG" ]; then 
  echo "No specific tag entered. Here are the tagged repo images on GCP: "; 
  gcloud container images list-tags $REPOSITORY
  echo "Enter new version tag: (or CTRL+C to exit)"; 
  read $VERSION_TAG
  echo "Building image..."
  ${SUDO} gcloud builds submit --tag ${REPOSITORY}:${VERSION_TAG}
else 
  echo "Building image with tag version: '$VERSION_TAG'..."; 
  ${SUDO} gcloud builds submit --tag ${REPOSITORY}:${VERSION_TAG}
fi

# push to cloud run
if [[ ${DEPLOY} == true ]]; then
    echo "Pushing image to GCP Cloud Run..."
    gcloud run deploy covid-helpline --image ${REPOSITORY}:${VERSION_TAG} --platform managed --region us-central1 
fi

# cleanup
${SUDO} docker rmi -f ${REPOSITORY}/ch:${VERSION_TAG}


