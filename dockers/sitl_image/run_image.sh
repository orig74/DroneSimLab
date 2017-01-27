#!/bin/bash
#xhost + local:

#ARDU_PATH=`cd ../../ardupilot && pwd`
#echo $ARDU_PATH
#docker run -it --rm --name sitl_run -v $ARDU_PATH:/ardupilot -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY sitl_image /bin/bash
DRONE_LAB_DIR=`cd ../../ && pwd`

docker run -it --rm  \
-v $DRONE_LAB_DIR:/dronelab  \
-v /tmp/.X11-unix:/tmp/.X11-unix \
-v $DRONE_LAB_DIR/dockers/docker_home:/home/docker \
-e DISPLAY=$DISPLAY \
-e USERNAME=docker \
-e USER=docker \
-e SITL_POSITION_PORT=19988 \
-e HOME=/home/docker \
-u $UID \
sitl_image "/bin/bash"
#cd /dronelab/ardupilot/ArduCopter/ && ../Tools/autotest/sim_vehicle.py -w
