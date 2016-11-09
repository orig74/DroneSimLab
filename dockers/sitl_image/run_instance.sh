#!/bin/bash

#ARDU_PATH=`cd ../../ardupilot && pwd`
#echo $ARDU_PATH
#docker run -it --rm --name sitl_run -v $ARDU_PATH:/ardupilot -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY sitl_image /bin/bash
docker ps -all |grep sitl_run$2 | awk -- '{ print $1 }' | xargs docker stop
docker run -it --rm --name sitl_run$2 \
-v $1:/ardupilot  \
-e USERNAME=docker \
-e USER=docker \
-e SITL_POSITION_PORT=$( expr 19988 + 10 \* $2 ) \
-u $UID \
--net=host \
sitl_image /bin/bash -c \
"cd /ardupilot/ArduCopter/ && ../Tools/autotest/sim_vehicle.py -w -I $2"
