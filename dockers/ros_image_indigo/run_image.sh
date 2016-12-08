#!/bin/bash
xhost + local:

#ARDU_PATH=`cd ../../ardupilot && pwd`
#echo $ARDU_PATH
#docker run -it --rm --name sitl_run -v $ARDU_PATH:/ardupilot -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY sitl_image /bin/bash
docker run -it --rm --name ros_indigo \
-v /local/dronelabdata/PX4:/PX4  \
-v /tmp/.X11-unix:/tmp/.X11-unix \
-e DISPLAY=$DISPLAY \
-e USERNAME=docker \
-e USER=docker \
-e HOME=/home/docker \
-v $HOME:/myhome \
-v /local/dockerhome:/home/docker \
-u $UID \
--privileged \
ros_image_indigo "/bin/bash"

#--net host \
#make posix_sitl_default jmavsim

