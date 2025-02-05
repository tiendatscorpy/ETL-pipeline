#!/usr/bin/env bash

if [ -z "$1" ] || [ -z "$2" ]
  then
    echo "Missing arguments"
    exit 1
fi

input_path="$1"
output_path="$2"

if [ ! -d $input_path ] || [ ! -d $output_path ]
  then
    echo "Directory not exist"
    exit 1
fi

if (! docker stats --no-stream )
  then
    echo "Docker daemon is not runnning"
    exit 1
fi

docker volume create \
--driver local \
-o o=bind \
-o type=none \
-o device=$input_path \
input_folder 

docker volume create \
--driver local \
-o o=bind \
-o type=none \
-o device=$output_path \
output_folder

docker-compose up -d
exit 0