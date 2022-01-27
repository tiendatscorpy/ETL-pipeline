#!/usr/bin/env bash
docker-compose down --volumes --remove-orphans 
docker volume rm input_folder output_folder
echo "Clean up completed"
exit 0