#!/bin/bash

#ARDU_PATH=`cd ../../ardupilot && pwd`
#echo $ARDU_PATH
#docker run -it --rm --name sitl_run -v $ARDU_PATH:/ardupilot -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY sitl_image /bin/bash
( docker ps | grep sitl_run ) && docker rm sitl_run
docker run -it --rm --name sitl_run \
-v /local/dronelabdata/ardupilot:/ardupilot  \
-e USERNAME=docker \
-e USER=docker \
-e SITL_POSITION_PORT=$( expr 19988 + 10 \* $1 ) \
-u $UID \
--net=host \
sitl_image /bin/bash -c \
"cd /ardupilot/ArduCopter/ && ../Tools/autotest/sim_vehicle.py -w -I $1"
