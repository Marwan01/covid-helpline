#!/bin/bash
REPOSITORY=gcr.io/covid-helpline/covid-helpline
GCPLOGIN=true
COMMITPUSH=false

while getopts "nchdot:i:" opt; do
  case ${opt} in
    h)
      echo "Available optional arguments:
      -h : help
      -n : no gcloud login
      -c : commit and push code
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
          echo "Using tag: $OPTARG"
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

# login to GCP
if [[ ${GCPLOGIN} == true ]]; then
  echo "Login to GCP:" 
  ${SUDO} gcloud auth login
fi

# commit and push code to Github
if [[ ${COMMITPUSH} == true ]]; then
  echo "Committing and pushing your local changes...." 
  ${SUDO} git add *
  ${SUDO} git commit -m "commit via deploy script"
  ${SUDO} git push
fi

# build image
echo "Building image..."
${SUDO} gcloud builds submit --tag ${REPOSITORY}/ch:${VERSION_TAG}

# push to cloud run
if [[ ${DEPLOY} == true ]]; then
    echo "Deploying branch:" $(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')
    echo "Pushing image to GCP Cloud Run..."
    gcloud run deploy covid-helpline --image ${REPOSITORY}/ch:${VERSION_TAG} --platform managed --region us-central1 
fi

# cleanup
${SUDO} docker rmi -f ${REPOSITORY}/ch:${VERSION_TAG} || true


