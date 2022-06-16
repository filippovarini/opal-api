#!/bin/bash
imageName=opal-api
containerName=opal-api-container
port=8000

echo Delete old image...
docker image rm -f $imageName

docker build -t $imageName -f Dockerfile .

echo Delete old container...
docker rm -f $containerName

echo Run new container...
if [[ -z $ES_API ]]; then
  echo Run new container with .env file...
  docker run --env-file ./.env --name $containerName -p $port:$port $imageName
else
  echo Run new container with environment variables already set...
  docker run --name $containerName -p $port:$port $imageName
fi
