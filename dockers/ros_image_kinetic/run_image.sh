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
# removed -v $DRONE_LAB_DIR/ros/catkin_mavros:/ros/catkin_mavros \
docker run -it --rm --name ros_kinetic \
-v $DRONE_LAB_DIR:/DroneLab  \
-v $DRONE_LAB_DIR/dockers/docker_home:/home/docker \
-v $DRONE_LAB_DIR/ros/catkin_ws:/ros/catkin_ws \
-v `readlink -f ~`:/home/host \
-v /tmp/.X11-unix:/tmp/.X11-unix \
-e DISPLAY=$DISPLAY \
-e USERNAME=docker \
-e USER=docker \
-e HOME=/home/docker \
-u $UID \
-p 10000-10100:10000-10100/udp \
-p 10200-10300:10200-10300 \
--privileged \
ros_image_kinetic "/bin/bash" $@

#--net host \
#make posix_sitl_default jmavsim

