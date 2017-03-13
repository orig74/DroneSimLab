#!/bin/bash
#source /opt/ros/kinetic/setup.bash
if [ -e /opt/ros/indigo/setup.bash ] 
then
	source /opt/ros/indigo/setup.bash
fi

if [ -e /opt/ros/kinetic/setup.bash ] 
then
	source /opt/ros/kinetic/setup.bash
fi

#ROS_PACKAGE_PATH=/ros/catkin_ws/src:/ros/catkin_mavros/src:$ROS_PACKAGE_PATH
#source /opt/ros/indigo/setup.bash
cd ~
