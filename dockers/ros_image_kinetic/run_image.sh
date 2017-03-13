#!/bin/bash
xhost + local:

DRONE_LAB_DIR=`python -c "import os;print(os.path.abspath(os.path.dirname('$0/../../../')))"`
#WORKSAPCE=~/projects
echo "----------------"
echo $DRONE_LAB_DIR

## 
#echo "if you get errors like docker: Error response from daemon: mkdir ....: permission denied."
#echo "try to 'chmod o+x thedir' and the ../"

chmod o+x $DRONE_LAB_DIR
chmod o+x $DRONE_LAB_DIR/dockers
##
docker run -it --rm --name ros_indigo \
-v $DRONE_LAB_DIR:/DroneLab  \
-v $DRONE_LAB_DIR/dockers/docker_home:/home/docker \
-v $DRONE_LAB_DIR/ros/catkin_mavros:/ros/catkin_mavros \
-v $DRONE_LAB_DIR/ros/catkin_ws:/ros/catkin_ws \
-v /tmp/.X11-unix:/tmp/.X11-unix \
-e DISPLAY=$DISPLAY \
-e USERNAME=docker \
-e USER=docker \
-e HOME=/home/docker \
-u $UID \
--privileged \
ros_image_kinetic "/bin/bash" $@

#--net host \
#make posix_sitl_default jmavsim

