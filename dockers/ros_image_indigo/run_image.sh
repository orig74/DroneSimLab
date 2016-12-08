#!/bin/bash
xhost + local:

#DRONE_LAB_DIR=`python -c "import os;print os.path.abspath(os.path.dirname('$0/../../../'))"`
WORKSAPCE=~/projects


docker run -it --rm --name ros_indigo \
-v $WORKSAPCE:/workspace  \
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

