#!/bin/bash
xhost + local:

#ARDU_PATH=`cd ../../ardupilot && pwd`
#echo $ARDU_PATH
#docker run -it --rm --name sitl_run -v $ARDU_PATH:/ardupilot -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY sitl_image /bin/bash
docker run -it --rm --name sitl_run \
-v /local/dronelabdata/ardupilot:/ardupilot  \
-v /tmp/.X11-unix:/tmp/.X11-unix \
-e DISPLAY=$DISPLAY \
-e USERNAME=docker \
-e USER=docker \
-u $UID \
sitl_image "/bin/bash"
