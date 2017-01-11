#!/bin/bash
#http://stackoverflow.com/questions/10953953/ensuring-relative-git-paths
#find -type f -name .git -exec bash -c 'f="{}"; cd $(dirname $f); echo "gitdir: $(realpath --relative-to=. $(cut -d" " -f2 .git))" > .git' \;

DRONE_LAB_DIR=`cd ../../ && pwd`
#echo $ARDU_PATH
#docker run -it --rm --name sitl_run -v $ARDU_PATH:/ardupilot -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY sitl_image /bin/bash
docker ps -all |grep sitl_run$1 | awk -- '{ print $1 }' | xargs docker stop
docker ps -all |grep sitl_run$1 | awk -- '{ print $1 }' | xargs docker rm 
docker run -it --rm --name sitl_run$1 \
-v $DRONE_LAB_DIR:/dronelab  \
-e USERNAME=docker \
-e USER=docker \
-e SITL_POSITION_PORT=$( expr 19988 + 10 \* $1 ) \
-u $UID \
--net=host \
sitl_image /bin/bash \
-c "cd /dronelab/ardupilot/ArduCopter/ && ../Tools/autotest/sim_vehicle.py -w -I $1"



