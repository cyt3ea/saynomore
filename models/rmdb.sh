#!/bin/bash

#MUST give permissions using command : chmod +x (path to shell file)
#Run this to get rid of the old database for a new docker-compose up command

docker start mysql
docker start mysql-cmdline
sudo rm -rf webapp/migrations