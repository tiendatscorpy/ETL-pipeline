#!/usr/bin/env bash

input_path="$1"
output_path="$2"
if [ ! -d $input_path ]; then
    echo "Directory $input_path not exist"
    exit 1
fi

if [ ! -d $output_path ]; then
    echo "Directory $output_path not exist"
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